from fastapi import APIRouter, UploadFile, File
import tempfile
from ..services.parser import parse_file
from ..services.shopify_service import find_product_by_handle, create_product
from ..services.merge_logic import merge_dict
from ..services.db import save_import, save_product

router = APIRouter()

@router.post("/products")
async def import_products(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    parsed = parse_file(path)
    results = []

    for item in parsed:
        product = item["product"]
        existing = find_product_by_handle(product["handle"])

        if existing:
            merged = merge_dict(existing[0], product)
            shopify_id = merged["id"]
            results.append({"updated": shopify_id})
            save_product(product, action="update", shopify_id=str(shopify_id))
        else:
            created = create_product(product)
            shopify_id = created["product"]["id"]
            results.append({"created": shopify_id})
            save_product(product, action="create", shopify_id=str(shopify_id))

    save_import(results, filename=file.filename)
    return {"summary": results}