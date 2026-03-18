import random
from datetime import date, timedelta

NOMBRES = [
    "Andres", "Daniela", "Edward", "Ana", "Luis", "Laura", "Sofia",
    "Pedro", "Camila", "Diego", "Valentina", "Jorge", "Miguel",
    "Paula", "Felipe", "Alejandra", "David", "Natalia",
]

APELLIDOS = [
    "Castillo", "Velasquez", "Quadros", "Martinez", "Garcia", "Hernandez",
    "Ramirez", "Torres", "Vargas", "Morales", "Castro", "Rojas",
    "Sanchez", "Diaz", "Romero", "Navarro", "Ruiz", "Mendoza",
]


def _fecha_aleatoria_ingreso():
    hoy = date.today()
    dias_atras = random.randint(30, 3650)
    return (hoy - timedelta(days=dias_atras)).isoformat()


def generar_empleados(n):
    empleados = []

    for indice in range(1, n + 1):
        empleados.append(
            {
                "id": indice,
                "nombres": random.choice(NOMBRES),
                "apellidos": f"{random.choice(APELLIDOS)} {random.choice(APELLIDOS)}",
                "salario_base": round(random.uniform(1300000, 4500000), 2),
                "documento": str(random.randint(10000000, 99999999)),
                "fecha_ingreso": _fecha_aleatoria_ingreso(),
            }
        )

    return empleados
