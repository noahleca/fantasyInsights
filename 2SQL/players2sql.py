import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/CSV/Players'

use = "use fantasyInsights;"

dropTableJugadores = "DROP TABLE IF EXISTS players;"

createTableJugadores = """
CREATE TABLE players (
    idJugador INT IDENTITY(1,1) PRIMARY KEY,
    nombreJugador VARCHAR(255),
    nombreEquipo VARCHAR(255),
    posicionJugador VARCHAR(255),
    minutosJugados FLOAT,
    goles FLOAT,
    asistencias FLOAT,
    asistenciasSinGol FLOAT,
    balonesArea FLOAT,
    penaltisProvocados FLOAT,
    penaltisParados FLOAT,
    paradas FLOAT,
    despejes FLOAT,
    penaltisFallados FLOAT,
    golesPropia FLOAT,
    golesContra FLOAT,
    tarjetasAmarillas FLOAT,
    tarjetasRojas FLOAT,
    tirosPuerta FLOAT,
    regates FLOAT,
    balonesRecuperados FLOAT,
    posesionesPerdidas FLOAT,
    penaltisCometidos FLOAT,
    puntosTotales INT,
    puntosPromedio FLOAT,
    valorMercadoMinimo INT,
    valorMercadoMaximo INT,
    valorMercadoReciente INT,
    tendenciaValorMercado VARCHAR(255)
);
"""
cursor.execute(use)
cursor.execute(dropTableJugadores)
cursor.execute(createTableJugadores)

# Definir la consulta de inserción
insert_query = """
INSERT INTO players (
    nombreJugador, nombreEquipo, posicionJugador, minutosJugados, goles, asistencias, asistenciasSinGol,
    balonesArea, penaltisProvocados, penaltisParados, paradas, despejes, penaltisFallados, golesPropia,
    golesContra, tarjetasAmarillas, tarjetasRojas, tirosPuerta, regates, balonesRecuperados, posesionesPerdidas,
    penaltisCometidos, puntosTotales, puntosPromedio, valorMercadoMinimo, valorMercadoMaximo, valorMercadoReciente,
    tendenciaValorMercado
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Recorrer el directorio y subdirectorios en busca de archivos CSV
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.csv'):
            csv_file_path = os.path.join(root, file)
            df = pd.read_csv(csv_file_path)

            for index, row in df.iterrows():
                # Utilizamos una lista de valores para asegurar el orden correcto
                values = [row['nombreJugador'], row['nombreEquipo'], row['posicionJugador'],
                          row['mins_played'], row['goals'], row['goal_assist'], row['offtarget_att_assist'],
                          row['pen_area_entries'], row['penalty_won'], row['penalty_save'], row['saves'],
                          row['effective_clearance'], row['penalty_failed'], row['own_goals'],
                          row['goals_conceded'], row['yellow_card'], row['second_yellow_card'],
                          row['red_card'], row['total_scoring_att'], row['won_contest'],
                          row['ball_recovery'], row['poss_lost_all'], row['penalty_conceded'],
                          row['puntosTotales'], row['puntosPromedio'], row['valorMercadoMinimo'],
                          row['valorMercadoMaximo'], row['valorMercadoReciente'], row['tendenciaValorMercado']]
                
                cursor.execute(insert_query, values)

# Confirmar y cerrar la conexión
conexion.commit()
conexion.close()

print('Inserciones completadas en la tabla players.')