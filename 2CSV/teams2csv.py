import json
import os
import pandas as pd
from tqdm import tqdm

# Directorio de entrada
input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/JSON/players'

# Directorio de salida
output_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/CSV/Teams'

# Lista para almacenar los IDs de los equipos
team_ids = []

# Obtener la lista de carpetas (cada carpeta contiene un solo JSON de jugador)
player_folders = [os.path.join(root, folder) for root, dirs, _ in os.walk(input_directory) for folder in dirs]

if not player_folders:
    print("No se encontraron carpetas de jugadores en el directorio de entrada.")
else:
    # Crear una barra de progreso con el estilo personalizado
    with tqdm(total=len(player_folders), desc='Progreso', bar_format="{l_bar}{bar}|", dynamic_ncols=True) as pbar:
        for player_folder in player_folders:
            # Obtener el nombre corto del equipo de la carpeta (nombre de la carpeta)
            short_name = os.path.basename(player_folder)

            # Obtener el nombre del archivo JSON en la carpeta del jugador
            json_file = next((f for f in os.listdir(player_folder) if f.endswith('.json')), None)

            if json_file:
                # Ruta completa del archivo JSON
                json_file_path = os.path.join(player_folder, json_file)

                # Leemos el archivo JSON
                with open(json_file_path, 'r') as f:
                    data = json.load(f)

                # Extraemos los datos necesarios
                name = data.get("team", {}).get("name", "")
                short_name = data.get("team", {}).get("shortName", "")

                # Crear directorio del equipo en el directorio de salida
                team_directory = os.path.join(output_directory, name)
                os.makedirs(team_directory, exist_ok=True)

                # Generar el nombre del archivo CSV
                csv_filename = f"{short_name.replace(' ', '_')}_{name.replace(' ', '_')}_CSV.csv"

                # Crear un DataFrame con nombres de columnas en formato "camelCase"
                df = pd.DataFrame({
                    "idEquipo": [len(team_ids) + 1],
                    "nombreEquipo": [name],
                    "nombreCortoEquipo": [short_name]
                })

                # Guardar el DataFrame como archivo CSV en el directorio del equipo en el directorio de salida
                csv_path = os.path.join(team_directory, csv_filename)
                df.to_csv(csv_path, index=False, encoding='utf-8')

                # Agregar el ID del equipo a la lista
                team_ids.append({"team_name": short_name, "team_id": len(team_ids) + 1})

                pbar.set_postfix({"Progreso": "Completado"})
                pbar.update(1)

# Crear DataFrame para los IDs de los equipos
ids_df = pd.DataFrame(team_ids)

# Guardar DataFrame de IDs como archivo CSV en el directorio de salida
ids_csv_path = os.path.join(output_directory, "teams_ids.csv")
ids_df.to_csv(ids_csv_path, index=False, encoding='utf-8')

# Proceso finalizado
print("CSV de los equipos y archivo de IDs generados correctamente.\n")