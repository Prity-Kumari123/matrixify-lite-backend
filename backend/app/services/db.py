import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_import(summary: dict, filename: str = None):
    payload = {
        "summary": summary,
        "filename": filename,
        "created_at": datetime.utcnow().isoformat()
    }
    return supabase.table("imports").insert(payload).execute()


def save_product(product: dict, action: str, shopify_id: str = None):
    payload = {
        "handle": product.get("handle"),
        "title": product.get("title"),
        "payload": product,
        "action": action,
        "shopify_id": shopify_id,
        "created_at": datetime.utcnow().isoformat()
    }
    return supabase.table("products").insert(payload).execute()