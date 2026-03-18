import json
import os


def generar_archivo_json(registros, nombre_archivo):
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

    with open(nombre_archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(registros, archivo_json, ensure_ascii=False, indent=4)

    print(f"Archivo '{nombre_archivo}' generado exitosamente.")
