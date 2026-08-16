import requests


BASE_URL = "https://world.openfoodfacts.org/api/v2"


def search_product_by_barcode(barcode):
    url = f"{BASE_URL}/product/{barcode}.json"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name", "Unknown product"),
        "brand": product.get("brands", "Unknown brand"),
        "barcode": barcode,
        "ingredients_text": product.get("ingredients_text", "")
    }