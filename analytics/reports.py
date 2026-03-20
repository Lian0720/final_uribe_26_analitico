from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _ensure_parent(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def export_table(records: list[dict], output_path: str | Path) -> None:
    path = _ensure_parent(output_path)
    pd.DataFrame(records).to_csv(path, index=False, encoding="utf-8")


def export_json(payload: dict | list, output_path: str | Path) -> None:
    path = _ensure_parent(output_path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=4)


def build_sales_summary(sales: list[dict]) -> dict:
    total_sales = len(sales)
    total_revenue = round(sum(sale["total_pagar"] for sale in sales), 2)
    total_items = sum(sale["total_productos_vendidos"] for sale in sales)
    unique_sellers = len({sale["vendedor"]["id"] for sale in sales})
    average_ticket = round(total_revenue / total_sales, 2) if total_sales else 0.0

    return {
        "total_ventas": total_sales,
        "ingresos_totales": total_revenue,
        "productos_vendidos": total_items,
        "vendedores_unicos": unique_sellers,
        "ticket_promedio": average_ticket,
    }


def build_sales_by_seller(sales: list[dict]) -> list[dict]:
    rows = []
    for sale in sales:
        rows.append(
            {
                "vendedor_id": sale["vendedor"]["id"],
                "vendedor": f'{sale["vendedor"]["nombres"]} {sale["vendedor"]["apellidos"]}',
                "total_venta": sale["total_pagar"],
                "productos_vendidos": sale["total_productos_vendidos"],
            }
        )

    if not rows:
        return []

    seller_df = pd.DataFrame(rows)
    grouped = (
        seller_df.groupby(["vendedor_id", "vendedor"], as_index=False)
        .agg(
            ventas=("total_venta", "count"),
            ingresos=("total_venta", "sum"),
            productos_vendidos=("productos_vendidos", "sum"),
            ticket_promedio=("total_venta", "mean"),
        )
        .sort_values(["ingresos", "ventas"], ascending=[False, False])
    )
    grouped["ingresos"] = grouped["ingresos"].round(2)
    grouped["ticket_promedio"] = grouped["ticket_promedio"].round(2)
    return grouped.to_dict(orient="records")


def build_sales_by_date(sales: list[dict]) -> list[dict]:
    rows = []
    for sale in sales:
        rows.append(
            {
                "fecha": sale["fecha"],
                "ventas": 1,
                "ingresos": sale["total_pagar"],
                "productos_vendidos": sale["total_productos_vendidos"],
            }
        )

    if not rows:
        return []

    daily_df = pd.DataFrame(rows)
    grouped = (
        daily_df.groupby("fecha", as_index=False)
        .agg(
            ventas=("ventas", "sum"),
            ingresos=("ingresos", "sum"),
            productos_vendidos=("productos_vendidos", "sum"),
        )
        .sort_values("fecha")
    )
    grouped["ingresos"] = grouped["ingresos"].round(2)
    return grouped.to_dict(orient="records")


def build_top_products(sales: list[dict]) -> list[dict]:
    rows = []
    for sale in sales:
        for product in sale["productos"]:
            rows.append(
                {
                    "id_producto": product["id_producto"],
                    "producto": product["producto"],
                    "categoria": product.get("categoria"),
                    "color": product.get("color"),
                    "talla": product["talla"],
                    "cantidad_vendida": product["cantidad_unitaria"],
                    "ingresos": product["total_producto"],
                }
            )

    if not rows:
        return []

    products_df = pd.DataFrame(rows)
    grouped = (
        products_df.groupby(["id_producto", "producto", "categoria", "color", "talla"], as_index=False)
        .agg(
            cantidad_vendida=("cantidad_vendida", "sum"),
            ingresos=("ingresos", "sum"),
        )
        .sort_values(["cantidad_vendida", "ingresos"], ascending=[False, False])
    )
    grouped["ingresos"] = grouped["ingresos"].round(2)
    return grouped.to_dict(orient="records")


def build_data_quality_report(employees_valid: list[dict], employees_invalid: list[dict],
                              sales_valid: list[dict], sales_invalid: list[dict]) -> dict:
    return {
        "empleados_validos": len(employees_valid),
        "empleados_invalidos": len(employees_invalid),
        "ventas_validas": len(sales_valid),
        "ventas_invalidas": len(sales_invalid),
    }
