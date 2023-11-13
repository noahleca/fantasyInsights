import os
import subprocess

# Directorios de los archivos .py
directories = [
    "2JSON",
    "2CSV",
    "2SQL"
]

# Función para ejecutar los archivos .py en un directorio dado
def execute_python_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                subprocess.run(["python", file_path])

# Ejecutar los archivos .py en el orden deseado
for directory in directories:
    directory_path = os.path.join("ruta/de/tu/proyecto", directory)  # Reemplaza con la ruta de tu proyecto
    execute_python_files(directory_path)