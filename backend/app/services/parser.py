import pandas as pd
import os

def parse_file(file_path: str):
    try:
        # Try CSV first
        df = pd.read_csv(file_path)
    except Exception:
        try:
            # If CSV fails, try Excel
            df = pd.read_excel(file_path, engine="openpyxl")
        except Exception:
            raise ValueError("Uploaded file is not a valid CSV or Excel file")

    df.columns = [c.strip() for c in df.columns]

    products = {}

    for _, row in df.iterrows():
        handle = row.get("Handle")
        title = row.get("Title")

        if not handle and not title:
            continue

        key = handle or title

        if key not in products:
            products[key] = {
                "product": {
                    "id": row.get("ID"),
                    "handle": handle,
                    "title": title,
                    "body_html": row.get("Body (HTML)"),
                    "vendor": row.get("Vendor"),
                    "product_type": row.get("Product Type"),
                    "tags": row.get("Tags"),
                },
                "variants": []
            }

        products[key]["variants"].append({
           "variant_id": row.get("Variant ID"),
            "sku": row.get("Variant SKU"),
            "price": float(row.get("Variant Price", 0) or 0),
            "compare_at_price": row.get("Variant Compare At Price"),
            "inventory_qty": int(row.get("Variant Inventory Qty", 0) or 0),
            "option1_name": row.get("Option1 Name"),
            "option1_value": row.get("Option1 Value"),
        })

    return list(products.values())
