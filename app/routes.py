import requests

from flask import Blueprint, jsonify, request

from app.inventory import inventory
from app.openfoodfacts import search_product_by_barcode


routes = Blueprint("routes", __name__)


@routes.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify({"inventory": inventory})


@routes.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Inventory item not found"}), 404


@routes.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    new_item = {
        "id": len(inventory) + 1,
        "product_name": data["product_name"],
        "brand": data["brand"],
        "barcode": data["barcode"],
        "price": data["price"],
        "stock": data["stock"],
        "ingredients_text": data.get("ingredients_text", "")
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


@routes.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item)

    return jsonify({"error": "Inventory item not found"}), 404


@routes.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Inventory item deleted successfully"
            })

    return jsonify({"error": "Inventory item not found"}), 404


@routes.route("/products/search", methods=["GET"])
def search_product():
    barcode = request.args.get("barcode")

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400

    try:
        product = search_product_by_barcode(barcode)
    except requests.RequestException:
        return jsonify({
            "error": "Unable to connect to OpenFoodFacts"
        }), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product)


@routes.route("/inventory/import", methods=["POST"])
def import_inventory_item():
    data = request.get_json()
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400

    try:
        product = search_product_by_barcode(barcode)
    except requests.RequestException:
        return jsonify({
            "error": "Unable to connect to OpenFoodFacts"
        }), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    new_item = {
        "id": len(inventory) + 1,
        "product_name": product["product_name"],
        "brand": product["brand"],
        "barcode": product["barcode"],
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
        "ingredients_text": product["ingredients_text"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201