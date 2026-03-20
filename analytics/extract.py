import pandas as pd
from sqlalchemy import text


EMPLOYEES_QUERY = text(
    """
    SELECT
        id,
        first_name,
        last_name,
        document,
        salary_base,
        hire_date,
        role
    FROM employees
    ORDER BY id
    """
)


SALES_FLAT_QUERY = text(
    """
    SELECT
        s.id AS sale_id,
        s.date AS sale_date,
        s.total_items,
        s.total AS sale_total,
        e.id AS seller_id,
        e.first_name AS seller_first_name,
        e.last_name AS seller_last_name,
        e.document AS seller_document,
        sd.id AS detail_id,
        p.id AS product_id,
        p.name AS product_name,
        p.category AS product_category,
        p.color AS product_color,
        sd.product_size,
        sd.quantity,
        sd.unit_price,
        sd.subtotal
    FROM sales s
    JOIN employees e ON e.id = s.seller_id
    JOIN sale_details sd ON sd.sale_id = s.id
    JOIN products p ON p.id = sd.product_id
    ORDER BY s.date, s.id, sd.id
    """
)


def fetch_employees_df(engine) -> pd.DataFrame:
    return pd.read_sql_query(EMPLOYEES_QUERY, engine)


def fetch_sales_flat_df(engine) -> pd.DataFrame:
    return pd.read_sql_query(SALES_FLAT_QUERY, engine)
