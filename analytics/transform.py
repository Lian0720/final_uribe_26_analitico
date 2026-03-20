from __future__ import annotations

from typing import Any


def _iso_date(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _to_number(value: Any) -> float:
    return round(float(value), 2)


def employees_from_df(df) -> list[dict]:
    employees = []

    for row in df.itertuples(index=False):
        employees.append(
            {
                "id": int(row.id),
                "nombres": row.first_name,
                "apellidos": row.last_name,
                "salario_base": _to_number(row.salary_base),
                "documento": str(row.document),
                "fecha_ingreso": _iso_date(row.hire_date),
                "rol": row.role,
            }
        )

    return employees


def sales_from_flat_df(df) -> list[dict]:
    if df.empty:
        return []

    sales = []
    grouped = df.groupby("sale_id", sort=False)

    for sale_id, sale_rows in grouped:
        first_row = sale_rows.iloc[0]
        details = []

        for row in sale_rows.itertuples(index=False):
            details.append(
                {
                    "id_detalle": int(row.detail_id),
                    "id_producto": int(row.product_id),
                    "producto": row.product_name,
                    "categoria": row.product_category,
                    "color": row.product_color,
                    "talla": row.product_size,
                    "cantidad_unitaria": int(row.quantity),
                    "precio_unitario": _to_number(row.unit_price),
                    "total_producto": _to_number(row.subtotal),
                }
            )

        sales.append(
            {
                "id": int(sale_id),
                "fecha": _iso_date(first_row.sale_date),
                "vendedor": {
                    "id": int(first_row.seller_id),
                    "nombres": first_row.seller_first_name,
                    "apellidos": first_row.seller_last_name,
                    "documento": str(first_row.seller_document),
                },
                "productos": details,
                "total_productos_vendidos": int(first_row.total_items),
                "total_pagar": _to_number(first_row.sale_total),
            }
        )

    return sales
