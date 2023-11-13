import pyodbc
import pandas as pd
import os

server = 'DESKTOP-P8S1J1M'
bd = 'fantasyInsights'

conexion = pyodbc.connect(driver='{SQL Server}', host=server, database=bd)
cursor = conexion.cursor()

# Consultas SQL
useAlineaciones = "use fantasyInsights;"

dropTableAlineaciones = "DROP TABLE IF EXISTS lineups;"

createTableAlineaciones = """
    CREATE TABLE lineups (
        idLineup INT IDENTITY(1,1) PRIMARY KEY,
        nombreAlineacion VARCHAR(255),
        numeroPorteros INTEGER,
        numeroDefensas INTEGER,
        numeroCentrocampistas INTEGER,
        numeroDelanteros INTEGER
    );"""
    
cursor.execute(useAlineaciones)
cursor.execute(dropTableAlineaciones)
cursor.execute(createTableAlineaciones)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('5-4-1', 1, 5, 4, 1);"""
cursor.execute(insertAlineacion)
conexion.commit()
    
insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('5-3-2', 1, 5, 3, 2);"""
cursor.execute(insertAlineacion)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('4-5-1', 1, 4, 5, 1);"""
cursor.execute(insertAlineacion)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('4-4-2', 1, 4, 4, 2);"""
cursor.execute(insertAlineacion)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('4-3-3', 1, 4, 3, 3);"""
cursor.execute(insertAlineacion)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('3-5-2', 1, 3, 5, 2);"""
cursor.execute(insertAlineacion)
conexion.commit()

insertAlineacion = """
    INSERT INTO lineups (nombreAlineacion, numeroPorteros, numeroDefensas, numeroCentrocampistas, numeroDelanteros) 
    VALUES ('3-4-3', 1, 3, 4, 3);"""
cursor.execute(insertAlineacion)
conexion.commit()

print('Inserciones completadas en la tabla lineups.')
conexion.close()
    