import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

# Rutas
input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Managers/Players'

use = "use fantasyInsights;"

dropTableJugadores = "DROP TABLE IF EXISTS managers;"

createTableJugadores = """
CREATE TABLE managers (
    nombreUsuario VARCHAR(255),
    nombreLiga VARCHAR(255),
    nombreJugador VARCHAR(255),
    nombreEquipo VARCHAR(255),
    posicionId INTEGER,
    estadoJugador VARCHAR(255),
    clausula INTEGER,
    expiracionBloqueoClausulaDias INTEGER,
    valorMercado INTEGER,
    puntosRecientes INTEGER,
    puntosRecientesPromedio FLOAT,
    puntosTotales INTEGER
);
"""
cursor.execute(use)
cursor.execute(dropTableJugadores)
cursor.execute(createTableJugadores)
conexion.commit()

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.csv'):
            csv_file_path = os.path.join(root, file)
            print(f'Procesando archivo CSV: {csv_file_path}')
            
            data = pd.read_csv(csv_file_path)
            
            if all(col in data.columns for col in ["nombreUsuario", "nombreLiga", "nombreJugador"]):
                lista_valores = data.values.tolist()
                insert = """
INSERT INTO managers (nombreUsuario, nombreLiga, nombreJugador ,
                    nombreEquipo, posicionId, estadoJugador, 
                    clausula, expiracionBloqueoClausulaDias, valorMercado, 
                    puntosRecientes, puntosRecientesPromedio, puntosTotales) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

                cursor.executemany(insert, lista_valores)
                conexion.commit()
            else:
                print(f'No se pudo procesar el archivo CSV: {csv_file_path}')

# Commit para guardar los cambios
print('Inserciones completadas en la tabla stats.')
conexion.close()