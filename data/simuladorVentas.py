import random
from datetime import datetime, timedelta

from data.simuladorEmpleados import generar_empleados

PRODUCTOS = [
    {"nombre": "Camiseta", "precio_base": 45000, "tallas": ["XS", "S", "M", "L", "XL", "XXL"]},
    {"nombre": "Pantalon", "precio_base": 85000, "tallas": ["28", "30", "32", "34", "36", "38", "40"]},
    {"nombre": "Chaqueta", "precio_base": 120000, "tallas": ["S", "M", "L", "XL", "XXL"]},
    {"nombre": "Vestido", "precio_base": 98000, "tallas": ["S", "M", "L", "XL"]},
    {"nombre": "Zapatos", "precio_base": 135000, "tallas": ["36", "37", "38", "39", "40", "41", "42"]},
    {"nombre": "Gorra", "precio_base": 30000, "tallas": ["Unica"]},
    {"nombre": "Sudadera", "precio_base": 110000, "tallas": ["S", "M", "L", "XL", "XXL"]},
]


def _fecha_venta_aleatoria():
    return (datetime.now() - timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")


def _precio_unitario(precio_base):
    variacion = random.uniform(0.85, 1.30)
    return round(precio_base * variacion, 2)


def _generar_detalle_producto(indice_detalle):
    producto_base = random.choice(PRODUCTOS)
    cantidad = random.randint(1, 6)
    precio_unitario = _precio_unitario(producto_base["precio_base"])
    total_producto = round(cantidad * precio_unitario, 2)

    return {
        "id_detalle": indice_detalle,
        "id_producto": random.randint(1000, 9999),
        "producto": producto_base["nombre"],
        "talla": random.choice(producto_base["tallas"]),
        "cantidad_unitaria": cantidad,
        "precio_unitario": precio_unitario,
        "total_producto": total_producto,
    }


def generar_ventas(n, vendedores=None):
    if vendedores is None:
        vendedores = generar_empleados(max(5, min(n, 20)))

    ventas = []

    for id_venta in range(1, n + 1):
        cantidad_productos = random.randint(1, 5)
        detalles = [_generar_detalle_producto(indice + 1) for indice in range(cantidad_productos)]
        vendedor = random.choice(vendedores)
        total_venta = round(sum(item["total_producto"] for item in detalles), 2)

        ventas.append(
            {
                "id": id_venta,
                "fecha": _fecha_venta_aleatoria(),
                "vendedor": {
                    "id": vendedor["id"],
                    "nombres": vendedor["nombres"],
                    "apellidos": vendedor["apellidos"],
                    "documento": vendedor["documento"],
                },
                "productos": detalles,
                "total_productos_vendidos": sum(item["cantidad_unitaria"] for item in detalles),
                "total_pagar": total_venta,
            }
        )

    return ventas
