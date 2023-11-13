import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Teams'

use = "use fantasyInsights;"

dropTableTeams = 'DROP TABLE IF EXISTS teams;'

createTableTeams = """
                CREATE TABLE teams (
                    idEquipo INTEGER,
                    nombreEquipo VARCHAR(255),
                    nombreCortoEquipo VARCHAR(255)
                    );
                """

cursor.execute(use)
cursor.execute(dropTableTeams)
cursor.execute(createTableTeams)

cursor.commit()

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.csv'):
            csv_file_path = os.path.join(root, file)
            print(f'Procesando archivo CSV: {csv_file_path}')
            
            data = pd.read_csv(csv_file_path)
            
            if all(col in data.columns for col in ["nombreEquipo", "nombreCortoEquipo"]):
                lista_valores = data.values.tolist()
                insert = """
                    INSERT INTO teams (idEquipo, nombreEquipo, nombreCortoEquipo)
                    VALUES (?, ?, ?);
                    """
                cursor.executemany(insert, lista_valores)
                conexion.commit()
                print(f'Procesado el archivo CSV: {csv_file_path}')
            else:
                print(f'No se pudo procesar el archivo CSV: {csv_file_path}')
                
print('Inserciones completadas en la tabla coaches.')
conexion.close()
