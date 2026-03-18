import pandas as pd

from data.simuladorEmpleados import generar_empleados
from data.simuladorVentas import generar_ventas
from utils.generarCSV import generar_archivo_csv
from utils.generarJSON import generar_archivo_json

lista_empleados = generar_empleados(25)
lista_ventas = generar_ventas(200, lista_empleados)

generar_archivo_csv(lista_empleados, "data/empleados_simulados.csv")
generar_archivo_json(lista_empleados, "data/empleados_simulados.json")

generar_archivo_csv(lista_ventas, "data/ventas_simuladas.csv")
generar_archivo_json(lista_ventas, "data/ventas_simuladas.json")

df_ventas = pd.DataFrame(
    [
        {
            "id_venta": venta["id"],
            "fecha": venta["fecha"],
            "vendedor": f'{venta["vendedor"]["nombres"]} {venta["vendedor"]["apellidos"]}',
            "productos": len(venta["productos"]),
            "total_pagar": venta["total_pagar"],
        }
        for venta in lista_ventas
    ]
)

print(df_ventas.head())
