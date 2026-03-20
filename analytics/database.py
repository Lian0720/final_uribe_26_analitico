from sqlalchemy import inspect
from sqlalchemy import create_engine

from analytics.config import DatabaseConfig


EXPECTED_TABLES = {"employees", "products", "sales", "sale_details"}


def create_db_engine(config: DatabaseConfig):
    return create_engine(config.sqlalchemy_url(), future=True)


def validate_schema(engine, schema: str) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names(schema=schema))
    missing = EXPECTED_TABLES - table_names

    if missing:
        missing_tables = ", ".join(sorted(missing))
        raise RuntimeError(
            "La base de datos no tiene todas las tablas esperadas. "
            f"Faltan: {missing_tables}. Arranca el backend o revisa permisos del usuario."
        )
