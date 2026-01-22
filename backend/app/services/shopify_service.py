import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHOP = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
VERSION = os.getenv("SHOPIFY_API_VERSION")

BASE_URL = f"https://{SHOP}/admin/api/{VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}


def get_products():
    url = f"{BASE_URL}/products.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def find_product_by_handle(handle):
    url = f"{BASE_URL}/products.json?handle={handle}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    products = response.json().get("products", [])
    return products if products else None


def create_product(product):
    url = f"{BASE_URL}/products.json"

    product_payload = {
        "product": {
            "title": product["title"],
            "body_html": product.get("body_html"),
            "vendor": product.get("vendor"),
            "product_type": product.get("product_type"),
            "tags": product.get("tags"),
            "variants": [
                {
                    "price": str(v["price"]),
                    "sku": v.get("sku"),
                    "inventory_quantity": v.get("inventory_qty"),
                    "option1": v.get("option1_value")
                }
                for v in product.get("variants", [])
            ]
        }
    }

    response = requests.post(url, headers=HEADERS, json=product_payload)

    if response.status_code != 201:
        print("Shopify error:", response.text)
        response.raise_for_status()

    return response.json()
