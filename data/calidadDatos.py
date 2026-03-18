import copy
import random
from datetime import datetime


def _seleccionar_indices(total_registros, porcentaje):
    if total_registros <= 0:
        return []

    cantidad = max(1, int(total_registros * porcentaje))
    cantidad = min(cantidad, total_registros)
    return random.sample(range(total_registros), cantidad)


def _ensuciar_texto(texto):
    transformacion = random.choice(["espacios", "mayusculas", "numeros"])
    if transformacion == "espacios":
        return f"  {texto}  "
    if transformacion == "mayusculas":
        return texto.upper()
    return f"{texto}{random.randint(1, 99)}"


def _detalle_venta_es_valido(detalle):
    if not isinstance(detalle.get("producto"), str):
        return False
    if detalle["producto"].strip() != detalle["producto"]:
        return False
    if detalle["producto"] != detalle["producto"].title():
        return False
    if detalle.get("cantidad_unitaria", 0) <= 0:
        return False
    if detalle.get("precio_unitario", 0) <= 0:
        return False
    if detalle.get("total_producto", 0) <= 0:
        return False
    return True


def _empleado_es_valido(empleado):
    nombres = empleado.get("nombres", "")
    apellidos = empleado.get("apellidos", "")
    documento = str(empleado.get("documento", ""))

    if not isinstance(nombres, str) or nombres.strip() != nombres or not nombres.replace(" ", "").isalpha():
        return False
    if not isinstance(apellidos, str) or apellidos.strip() != apellidos or not apellidos.replace(" ", "").isalpha():
        return False
    if empleado.get("salario_base", 0) <= 0:
        return False
    if not documento.isdigit():
        return False

    try:
        datetime.strptime(empleado.get("fecha_ingreso", ""), "%Y-%m-%d")
    except ValueError:
        return False

    return True


def _venta_es_valida(venta):
    productos = venta.get("productos", [])
    vendedor = venta.get("vendedor", {})

    if not productos:
        return False
    if not vendedor:
        return False
    if not all(_detalle_venta_es_valido(detalle) for detalle in productos):
        return False
    if venta.get("total_productos_vendidos", 0) <= 0:
        return False
    if venta.get("total_pagar", 0) <= 0:
        return False

    try:
        datetime.strptime(venta.get("fecha", ""), "%Y-%m-%d")
    except ValueError:
        return False

    total_cantidades = sum(detalle["cantidad_unitaria"] for detalle in productos)
    total_productos = round(sum(detalle["total_producto"] for detalle in productos), 2)

    if venta["total_productos_vendidos"] != total_cantidades:
        return False
    if round(venta["total_pagar"], 2) != total_productos:
        return False

    return True


def ensuciar_empleados(empleados, porcentaje=0.30):
    empleados_sucios = copy.deepcopy(empleados)

    for indice in _seleccionar_indices(len(empleados_sucios), porcentaje):
        empleado = empleados_sucios[indice]
        tipo_error = random.choice(
            [
                "nombre_con_espacios",
                "nombre_con_numeros",
                "apellido_mayusculas",
                "documento_invalido",
                "salario_negativo",
            ]
        )

        if tipo_error == "nombre_con_espacios":
            empleado["nombres"] = f"  {empleado['nombres']}  "
        elif tipo_error == "nombre_con_numeros":
            empleado["nombres"] = f"{empleado['nombres']}{random.randint(1, 9)}"
        elif tipo_error == "apellido_mayusculas":
            empleado["apellidos"] = empleado["apellidos"].upper()
        elif tipo_error == "documento_invalido":
            empleado["documento"] = f"A{empleado['documento']}"
        else:
            empleado["salario_base"] = -abs(float(empleado["salario_base"]))

    return empleados_sucios


def limpiar_empleados(empleados):
    empleados_limpios = []
    empleados_retirados = []

    for empleado in empleados:
        if _empleado_es_valido(empleado):
            empleados_limpios.append(copy.deepcopy(empleado))
        else:
            registro = copy.deepcopy(empleado)
            registro["motivo_descarte"] = "empleado_invalido"
            empleados_retirados.append(registro)

    return empleados_limpios, empleados_retirados


def ensuciar_ventas(ventas, porcentaje=0.30):
    ventas_sucias = copy.deepcopy(ventas)

    for indice in _seleccionar_indices(len(ventas_sucias), porcentaje):
        venta = ventas_sucias[indice]
        tipo_error = random.choice(
            [
                "cantidad_negativa",
                "producto_en_mayusculas",
                "producto_con_espacios",
                "precio_negativo",
                "total_inconsistente",
            ]
        )
        detalle = random.choice(venta["productos"])

        if tipo_error == "cantidad_negativa":
            detalle["cantidad_unitaria"] = -abs(int(detalle["cantidad_unitaria"]))
        elif tipo_error == "producto_en_mayusculas":
            detalle["producto"] = detalle["producto"].upper()
        elif tipo_error == "producto_con_espacios":
            detalle["producto"] = f"  {detalle['producto']}  "
        elif tipo_error == "precio_negativo":
            detalle["precio_unitario"] = -abs(float(detalle["precio_unitario"]))
        else:
            venta["total_pagar"] = -abs(float(venta["total_pagar"]))

    return ventas_sucias


def limpiar_ventas(ventas):
    ventas_limpias = []
    ventas_retiradas = []

    for venta in ventas:
        if _venta_es_valida(venta):
            ventas_limpias.append(copy.deepcopy(venta))
        else:
            registro = copy.deepcopy(venta)
            registro["motivo_descarte"] = "venta_invalida"
            ventas_retiradas.append(registro)

    return ventas_limpias, ventas_retiradas
