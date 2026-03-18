import os

import pandas as pd


def _normalizar_registros_para_csv(registros):
    if not registros:
        return []

    primer_registro = registros[0]
    if "productos" not in primer_registro:
        return registros

    filas = []
    for venta in registros:
        vendedor = venta.get("vendedor", {})
        for producto in venta.get("productos", []):
            filas.append(
                {
                    "id_venta": venta.get("id"),
                    "fecha": venta.get("fecha"),
                    "vendedor_id": vendedor.get("id"),
                    "vendedor_nombres": vendedor.get("nombres"),
                    "vendedor_apellidos": vendedor.get("apellidos"),
                    "vendedor_documento": vendedor.get("documento"),
                    "id_detalle": producto.get("id_detalle"),
                    "id_producto": producto.get("id_producto"),
                    "producto": producto.get("producto"),
                    "talla": producto.get("talla"),
                    "cantidad_unitaria": producto.get("cantidad_unitaria"),
                    "precio_unitario": producto.get("precio_unitario"),
                    "total_producto": producto.get("total_producto"),
                    "total_productos_vendidos": venta.get("total_productos_vendidos"),
                    "total_pagar": venta.get("total_pagar"),
                }
            )

    return filas


def generar_archivo_csv(registros, nombre_archivo):
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
    datos_csv = _normalizar_registros_para_csv(registros)
    df = pd.DataFrame(datos_csv)
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    print(f"Archivo '{nombre_archivo}' generado exitosamente.")
