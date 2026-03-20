import pandas as pd

from analytics.config import DatabaseConfig
from analytics.database import create_db_engine, validate_schema
from analytics.extract import fetch_employees_df, fetch_sales_flat_df
from analytics.reports import (
    build_data_quality_report,
    build_sales_by_date,
    build_sales_by_seller,
    build_sales_summary,
    build_top_products,
    export_json,
    export_table,
)
from analytics.transform import employees_from_df, sales_from_flat_df
from data.calidadDatos import limpiar_empleados, limpiar_ventas
from utils.generarCSV import generar_archivo_csv
from utils.generarJSON import generar_archivo_json


def main() -> None:
    config = DatabaseConfig.from_env()
    engine = create_db_engine(config)
    validate_schema(engine, config.schema)

    employees_df = fetch_employees_df(engine)
    sales_flat_df = fetch_sales_flat_df(engine)

    employees = employees_from_df(employees_df)
    sales = sales_from_flat_df(sales_flat_df)

    clean_employees, invalid_employees = limpiar_empleados(employees)
    clean_sales, invalid_sales = limpiar_ventas(sales)

    generar_archivo_csv(clean_employees, "data/reportes/empleados_bd.csv")
    generar_archivo_json(clean_employees, "data/reportes/empleados_bd.json")

    generar_archivo_csv(clean_sales, "data/reportes/ventas_bd.csv")
    generar_archivo_json(clean_sales, "data/reportes/ventas_bd.json")

    generar_archivo_csv(invalid_employees, "data/reportes/empleados_invalidos.csv")
    generar_archivo_csv(invalid_sales, "data/reportes/ventas_invalidas.csv")

    sales_summary = build_sales_summary(clean_sales)
    sales_by_seller = build_sales_by_seller(clean_sales)
    sales_by_date = build_sales_by_date(clean_sales)
    top_products = build_top_products(clean_sales)
    quality_report = build_data_quality_report(
        clean_employees,
        invalid_employees,
        clean_sales,
        invalid_sales,
    )

    export_json(sales_summary, "data/reportes/resumen_ventas.json")
    export_json(quality_report, "data/reportes/calidad_datos.json")
    export_table(sales_by_seller, "data/reportes/ventas_por_vendedor.csv")
    export_json(sales_by_seller, "data/reportes/ventas_por_vendedor.json")
    export_table(sales_by_date, "data/reportes/ventas_por_fecha.csv")
    export_json(sales_by_date, "data/reportes/ventas_por_fecha.json")
    export_table(top_products, "data/reportes/top_productos.csv")
    export_json(top_products, "data/reportes/top_productos.json")
    export_json(
        {
            "resumen": sales_summary,
            "calidad_datos": quality_report,
            "ventas_por_vendedor": sales_by_seller,
            "ventas_por_fecha": sales_by_date,
            "top_productos": top_products,
        },
        "data/reportes/dashboard_front.json",
    )

    dashboard_df = pd.DataFrame(
        [
            {
                "id_venta": sale["id"],
                "fecha": sale["fecha"],
                "vendedor": f'{sale["vendedor"]["nombres"]} {sale["vendedor"]["apellidos"]}',
                "productos": len(sale["productos"]),
                "total_pagar": sale["total_pagar"],
            }
            for sale in clean_sales
        ]
    )

    print("Conexion a PostgreSQL exitosa.")
    print(dashboard_df.head())
    print(
        "Reporte generado en data/reportes | "
        f"Empleados validos: {len(clean_employees)} | "
        f"Ventas validas: {len(clean_sales)}"
    )


if __name__ == "__main__":
    main()
