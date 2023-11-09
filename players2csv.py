import json
import os
import pandas as pd
from tqdm import tqdm

# Directorio de entrada
input_directory = 'C:/Users/Noah Lecegui/Documents/BD Fantasy/JSON/players'

# Directorio de salida
output_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/CSV/Players'

# Función para calcular la media de playerStats
def calculate_averages(player_stats_list):
    if not player_stats_list:
        return {field: 0 for field in ["mins_played", "goals", "goal_assist", "offtarget_att_assist",
                                        "pen_area_entries", "penalty_won", "penalty_save", "saves",
                                        "effective_clearance", "penalty_failed", "own_goals", "goals_conceded",
                                        "yellow_card", "second_yellow_card", "red_card", "total_scoring_att",
                                        "won_contest", "ball_recovery", "poss_lost_all"]}

    sums = {field: 0 for field in player_stats_list[0]["stats"].keys() if field != "marca_points"}
    num_players = len(player_stats_list)

    for player_stat in player_stats_list:
        for field, values in player_stat["stats"].items():
            if field != "marca_points":
                sums[field] += values[0]

    averages = {field: round(total / num_players, 2) for field, total in sums.items()}
    return averages

# Función para determinar la tendencia del valor de mercado
def market_value_trend(market_values):
    if len(market_values) < 2:
        return "N/A"
    if market_values[-1] > market_values[-2]:
        return "Sube"
    else:
        return "Baja"

# Obtener la lista de archivos JSON
json_files = [os.path.join(root, file) for root, _, files in os.walk(input_directory) for file in files if file.endswith('.json')]

if not json_files:
    print("No se encontraron archivos JSON en el directorio de entrada.")
else:
    # Crear una barra de progreso con el estilo personalizado
    with tqdm(total=len(json_files), desc='Progreso', bar_format="{l_bar}{bar}|", dynamic_ncols=True) as pbar:
        for json_file in json_files:
            # Leemos el archivo JSON
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Verificamos si el jugador es un entrenador y evitamos crear un archivo CSV
            position = data.get("position", "")
            if position.lower() == "entrenador":
                pbar.set_postfix({"Progreso": "Saltado"})
                pbar.update(1)
                continue
            
            # Establecemos valores predeterminados para los jugadores sin playerStats
            if not data.get("playerStats"):
                data["playerStats"] = [{
                    "stats": {
                        "mins_played": [0, 0],
                        "goals": [0, 0],
                        "goal_assist": [0, 0],
                        # Agregar más campos con valores predeterminados
                    }
                }]
            
            # Extraemos los datos necesarios
            name = data["name"]
            team_name = data["team"]["name"]
            
            # Traducción de la posición
            position = position[0].lower() + position[1:]
            
            player_stats_list = data.get("playerStats", [])
            averages = calculate_averages(player_stats_list)
            points_total = round(data["points"], 2)
            points_average = round(data["averagePoints"], 2)
            market_values = list(data["marketValue"].values())
            min_market_value = round(min(market_values), 2)
            max_market_value = round(max(market_values), 2)
            recent_market_value = round(market_values[-1], 2)
            market_trend = market_value_trend(market_values)
            
            # Crear directorio del equipo en el directorio de salida
            team_directory = os.path.join(output_directory, team_name)
            os.makedirs(team_directory, exist_ok=True)
            
            # Generar el nombre del archivo CSV
            csv_filename = f"{data['team']['shortName'].replace(' ', '_')}_{name.replace(' ', '_')}_CSV.csv"
            
            # Crear un DataFrame con nombres de columnas en formato "camelCase"
            df = pd.DataFrame({
                "nombreJugador": [name],
                "nombreEquipo": [team_name],
                "posicionJugador": [position],
                **averages,
                "puntosTotales": [points_total],
                "puntosPromedio": [points_average],
                "valorMercadoMinimo": [min_market_value],
                "valorMercadoMaximo": [max_market_value],
                "valorMercadoReciente": [recent_market_value],
                "tendenciaValorMercado": [market_trend]
            })
            
            # Guardar el DataFrame como archivo CSV en el directorio del equipo en el directorio de salida
            csv_path = os.path.join(team_directory, csv_filename)
            df.to_csv(csv_path, index=False, encoding='utf-8')
            pbar.set_postfix({"Progreso": ""})
            pbar.update(1)
        
    print("CSV de los jugadores generados correctamente.\n")