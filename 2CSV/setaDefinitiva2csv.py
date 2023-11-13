import os
import json
import pandas as pd
from datetime import datetime

input_directory = "C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/JSON/Mis ligas/mis_ligas/012818008"
output_base_directory = "C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Managers/Players/seta definitiva"

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.json') and file != 'market.json':
            json_file_path = os.path.join(root, file)
            print(f"Procesando el archivo JSON: {json_file_path}")
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                players_data = data.get("players")

                for player in players_data:
                    if "manager" in player and "playerMaster" in player:
                        manager_id = int(player["manager"]["id"])  # Asegura que sea un entero
                        manager_name = player["manager"]["managerName"]
                        nickname = player["playerMaster"]["nickname"]

                        clausula = player.get("buyoutClause", 0)
                        expiracion_bloqueo_clausula = player.get("buyoutClauseLockedEndTime", "")
                        valor_mercado = player["playerMaster"].get("marketValue", 0)


                        # Calcular la cantidad de días restantes en el bloqueo de la cláusula
                        if expiracion_bloqueo_clausula:
                            bloqueo_clausula_fecha = datetime.fromisoformat(expiracion_bloqueo_clausula[:-6])
                            dias_restantes = (bloqueo_clausula_fecha - datetime.now()).days
                            dias_restantes = dias_restantes if dias_restantes > 0 else 0  # Condición para establecer 0 si es menor o igual a 0
                        else:
                            dias_restantes = 0

                        if "lastStats" in player["playerMaster"]:
                            last_stats = player["playerMaster"]["lastStats"]
                            total_points = sum(stats.get("totalPoints", 0) for stats in last_stats)
                            points_count = len(last_stats)
                            recent_points = last_stats[-1].get("totalPoints", 0) if points_count > 0 else 0
                            average_points = round(total_points / points_count, 2) if points_count > 0 else 0
                        else:
                            total_points = 0
                            recent_points = 0
                            average_points = 0

                        nombreLiga = "seta definitiva" #CAMBIAR EL NOMBRE DE LA LIGA

                        # Definir el nombre del archivo CSV
                        file_name = f"{manager_name.replace(' ', '_')}_{nickname}_CSV.csv"

                        csv_data = {
                            "nombreUsuario": [manager_name],
                            "nombreLiga": nombreLiga,
                            "nombreJugador": [nickname],
                            "nombreEquipo": [player["playerMaster"]["team"]["name"]],
                            "posicionId": [player["playerMaster"]["positionId"]],
                            "estadoJugador": [player["playerMaster"]["playerStatus"]],
                            "clausula": [clausula],
                            "expiracionBloqueoClausulaDias": [dias_restantes],
                            "valorMercado": [valor_mercado],
                            "puntosRecientes": [recent_points],
                            "puntosRecientesPromedio": [average_points],
                            "puntosTotales": [total_points]
                        }

                        df = pd.DataFrame(csv_data)

                        directory_path = os.path.join(output_base_directory, manager_name)  # Directorio específico para el manager

                        os.makedirs(directory_path, exist_ok=True)
                        # Guardar el archivo en el directorio correspondiente
                        csv_file_path = os.path.join(directory_path, file_name)
                        df.to_csv(csv_file_path, index=False)
                        print(f"CSV de {file_name} generado correctamente.")