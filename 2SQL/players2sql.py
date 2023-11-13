import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

# Rutas
input_directory = 'C:/Users/Noah Lecegui/Documents/Fantasy Insights/Archivos/CSV/Players'

# Consultas SQL
use = "use fantasyInsights;"

dropTableJugadores = "DROP TABLE IF EXISTS players;"

createTableJugadores = """
CREATE TABLE players (
idJugador INT IDENTITY(1,1) PRIMARY KEY,
nombreJugador VARCHAR(255),
nombreEquipo VARCHAR(255),
posicionJugador VARCHAR(255),
mins_played FLOAT,
goals FLOAT,
goal_assist FLOAT,
offtarget_att_assist FLOAT,
pen_area_entries FLOAT,
penalty_won FLOAT,
penalty_save FLOAT,
saves FLOAT,
effective_clearance FLOAT,
penalty_failed FLOAT,
own_goals FLOAT,
goals_conceded FLOAT,
yellow_card FLOAT,
second_yellow_card FLOAT,
red_card FLOAT,
total_scoring_att FLOAT,
won_contest FLOAT,
ball_recovery FLOAT,
poss_lost_all FLOAT,
penalty_conceded FLOAT,
puntosTotales FLOAT,
puntosPromedio FLOAT,
weekNumber INTEGER,
weekPoints INTEGER,
valorMercadoMinimo INTEGER,
valorMercadoMaximo INTEGER,
valorMercadoReciente INTEGER,
tendenciaValorMercado VARCHAR(255)
);
"""

# Crear la tabla y el esquema
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
            
            if all(col in data.columns for col in ["nombreJugador", "nombreEquipo", "posicionJugador"]):
                lista_valores = data.values.tolist()
                insert = """
INSERT INTO players (nombreJugador, nombreEquipo, posicionJugador, mins_played, 
                    goals, goal_assist, offtarget_att_assist, pen_area_entries, penalty_won, 
                    penalty_save, saves, effective_clearance, penalty_failed, own_goals, 
                    goals_conceded, yellow_card, second_yellow_card, red_card, total_scoring_att, 
                    won_contest, ball_recovery, poss_lost_all, penalty_conceded, puntosTotales, 
                    puntosPromedio, weekNumber, weekPoints, valorMercadoMinimo, valorMercadoMaximo, valorMercadoReciente, tendenciaValorMercado) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


                cursor.executemany(insert, lista_valores)
                conexion.commit()
            else:
                print(f'No se pudo procesar el archivo CSV: {csv_file_path}')

# Commit para guardar los cambios
print('Inserciones completadas en la tabla stats.')
conexion.close()
