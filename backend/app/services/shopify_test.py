import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SHOP = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
VERSION = os.getenv("SHOPIFY_API_VERSION")

print("STORE:", SHOP)
print("TOKEN EXISTS:", bool(TOKEN))

url = f"https://{SHOP}/admin/api/{VERSION}/products.json"

headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response Preview:", response.text[:300])
