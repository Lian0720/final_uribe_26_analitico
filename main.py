import pandas as pd

from data.calidadDatos import (
    ensuciar_empleados,
    ensuciar_ventas,
    limpiar_empleados,
    limpiar_ventas,
)
from data.simuladorEmpleados import generar_empleados
from data.simuladorVentas import generar_ventas
from utils.generarCSV import generar_archivo_csv
from utils.generarJSON import generar_archivo_json

lista_empleados = generar_empleados(25)
lista_empleados_sucios = ensuciar_empleados(lista_empleados, porcentaje=0.30)
lista_empleados_limpios, empleados_descartados = limpiar_empleados(lista_empleados_sucios)

lista_ventas = generar_ventas(200, lista_empleados_limpios)
lista_ventas_sucias = ensuciar_ventas(lista_ventas, porcentaje=0.30)
lista_ventas_limpias, ventas_descartadas = limpiar_ventas(lista_ventas_sucias)

generar_archivo_csv(lista_empleados_limpios, "data/empleados_simulados.csv")
generar_archivo_json(lista_empleados_limpios, "data/empleados_simulados.json")

generar_archivo_csv(lista_ventas_limpias, "data/ventas_simuladas.csv")
generar_archivo_json(lista_ventas_limpias, "data/ventas_simuladas.json")

generar_archivo_csv(empleados_descartados, "data/datosSuciosEmpleados.csv")
generar_archivo_csv(ventas_descartadas, "data/datosSuciosVentas.csv")

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
print(f"Empleados limpios: {len(lista_empleados_limpios)} | Empleados descartados: {len(empleados_descartados)}")
print(f"Ventas limpias: {len(lista_ventas_limpias)} | Ventas descartadas: {len(ventas_descartadas)}")
