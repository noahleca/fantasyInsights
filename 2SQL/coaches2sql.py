import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

# Rutas
input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Coaches'

# Consultas SQL
use = "use fantasyInsights;"

dropTableCoaches = "DROP TABLE IF EXISTS coaches;"

createTableCoaches = """
                    CREATE TABLE coaches(
                        idEntrenador INT IDENTITY(1,1) PRIMARY KEY,
                        nombreEntrenador VARCHAR(255),
                        nombreEquipo VARCHAR(255),
                        won_match INTEGER,
                        lost_match INTEGER,
                        drawn_match INTEGER,
                        valorMercadoMinimo INTEGER,
                        valorMercadoMaximo INTEGER,
                        valorMercadoReciente INTEGER,
                        tendenciaValorMercado VARCHAR(255)
                        );
                    """

cursor.execute(use)
cursor.execute(dropTableCoaches)
cursor.execute(createTableCoaches)

cursor.commit()

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.csv'):
            csv_file_path = os.path.join(root, file)
            print(f'Procesando archivo CSV: {csv_file_path}')
            
            data = pd.read_csv(csv_file_path)
            
            if all(col in data.columns for col in ["nombreJugador", "nombreEquipo"]):
                lista_valores = data.values.tolist()
                insert = """
                        INSERT INTO coaches (nombreEntrenador, nombreEquipo, won_match, 
                        lost_match, drawn_match, valorMercadoMinimo, 
                        valorMercadoMaximo, valorMercadoReciente, tendenciaValorMercado)
                        VALUES (?,?,?,?,?,?,?,?,?);
                        """
                        
                cursor.executemany(insert, lista_valores)
                conexion.commit()
            else:
                print(f'No se pudo procesar el archivo CSV: {csv_file_path}')
                
print('Inserciones completadas en la tabla coaches.')
conexion.close()