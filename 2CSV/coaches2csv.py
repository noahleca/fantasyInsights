import json
import os
import pandas as pd
from tqdm import tqdm

# Directorio de entrada
input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/JSON/Jugadores/players'

# Directorio de salida
output_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Coaches'

# Función para determinar la tendencia del valor de mercado
def market_value_trend(market_values):
    if len(market_values) < 2:
        return "N/A"
    if market_values[-1] > market_values[-2]:
        return "Sube"
    else:
        return "Baja"

# Función para sumar los valores de "won_match", "lost_match" y "drawn_match"
def sum_match_stats(player_stats_list):
    if not player_stats_list:
        return {"won_match": 0, "lost_match": 0, "drawn_match": 0}

    sums = {field: 0 for field in ["won_match", "lost_match", "drawn_match"]}
    for player_stat in player_stats_list:
        for field, values in player_stat["stats"].items():
            if field in sums:
                sums[field] += values[0]

    return sums

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
            if position.lower() != "entrenador":
                pbar.set_postfix({"Progreso": "Saltado"})
                pbar.update(1)
                continue
            
            # Extraemos los datos necesarios
            name = data["name"]
            team_name = data["team"]["name"]
            market_values = list(data["marketValue"].values())
            recent_market_value = round(market_values[-1], 2)
            market_trend = market_value_trend(market_values)
            
            # Calculamos la suma de los valores de "won_match", "lost_match" y "drawn_match"
            match_stats_sum = sum_match_stats(data.get("playerStats", []))
            
            # Obtener el valor de mercado más alto y más bajo
            max_market_value = round(max(market_values), 2)
            min_market_value = round(min(market_values), 2)
            
            # Crear directorio del equipo en el directorio de salida
            team_directory = os.path.join(output_directory, team_name)
            os.makedirs(team_directory, exist_ok=True)
            
            # Generar el nombre del archivo CSV
            csv_filename = f"{data['team']['shortName'].replace(' ', '_')}_{name.replace(' ', '_')}_CSV.csv"
            
            # Eliminar el archivo CSV anterior si existe
            csv_path = os.path.join(team_directory, csv_filename)
            if os.path.exists(csv_path):
                os.remove(csv_path)
            
            # Crear un DataFrame con nombres de columnas en formato "camelCase"
            df = pd.DataFrame({
                "nombreJugador": [name],
                "nombreEquipo": [team_name],
                **match_stats_sum,  # Agregamos las sumas de los partidos ganados, perdidos y empatados
                "valorMercadoMinimo": [min_market_value],  # Agregamos el valor de mercado mínimo
                "valorMercadoMaximo": [max_market_value],  # Agregamos el valor de mercado máximo
                "valorMercadoReciente": [recent_market_value],
                "tendenciaValorMercado": [market_trend]
            })
            
            # Guardar el DataFrame como archivo CSV
            df.to_csv(csv_path, index=False)
            
            pbar.set_postfix({"Progreso": "Completado"})
            pbar.update(1)

# Proceso finalizado
print("CSV de los entrenadores generados correctamente.\n")
