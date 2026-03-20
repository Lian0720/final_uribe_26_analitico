# final_uribe_26_analitico

Proyecto de analitica con Python adaptado para leer datos reales desde PostgreSQL.

## Que hace ahora

El flujo principal ya no depende de simuladores. Ahora:

- se conecta a la base de datos del backend
- lee `employees`, `products`, `sales` y `sale_details`
- normaliza los datos al formato que ya usaba el proyecto
- valida calidad de datos
- genera reportes JSON y CSV listos para consumo posterior desde back o front

## Configuracion de base de datos

Por defecto el proyecto intenta conectarse a:

- host: `localhost`
- puerto: `5432`
- base de datos: `sellix_db`
- usuario: `store_user`
- clave: `sellix_2024`

Puedes cambiarlo con variables de entorno:

- `ANALYTICS_DB_HOST`
- `ANALYTICS_DB_PORT`
- `ANALYTICS_DB_NAME`
- `ANALYTICS_DB_USER`
- `ANALYTICS_DB_PASSWORD`
- `ANALYTICS_DB_SCHEMA`

Puedes partir de `.env.example` como referencia.

## Ejecucion

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta el proyecto:

```bash
python main.py
```

## Salidas generadas

Los archivos quedan en `data/reportes`:

- `empleados_bd.csv`
- `empleados_bd.json`
- `ventas_bd.csv`
- `ventas_bd.json`
- `empleados_invalidos.csv`
- `ventas_invalidas.csv`
- `resumen_ventas.json`
- `calidad_datos.json`
- `ventas_por_vendedor.csv`
- `ventas_por_vendedor.json`
- `ventas_por_fecha.csv`
- `ventas_por_fecha.json`
- `top_productos.csv`
- `top_productos.json`
- `dashboard_front.json`

