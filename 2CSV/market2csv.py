import os
import json
import pandas as pd

input_directory = "C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/JSON/Mis ligas/mis_ligas"
output_directory = "C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Managers/Players"
print("hola chulo")
# Recorrer el directorio en busca de archivos JSON
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.json') and file != 'market.json':
            json_file_path = os.path.join(root, file)
            print(f"Procesando el archivo JSON: {json_file_path}")
            with open(json_file_path, 'r') as f:
                data = json.load(f)
