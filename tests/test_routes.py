import pytest
from unittest.mock import patch

from app import create_app
from app.inventory import inventory

from app import routes


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def reset_inventory():
    inventory.clear()

    inventory.extend([
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "barcode": "0123456789012",
            "price": 450.00,
            "stock": 20,
            "ingredients_text": "Filtered water, almonds, cane sugar"
        },
        {
            "id": 2,
            "product_name": "Organic Oat Milk",
            "brand": "Oatly",
            "barcode": "0123456789013",
            "price": 500.00,
            "stock": 15,
            "ingredients_text": "Water, oats, rapeseed oil"
        }
    ])


def test_get_inventory(client):
    reset_inventory()

    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert "inventory" in data
    assert len(data["inventory"]) == 2


def test_get_inventory_item(client):
    reset_inventory()

    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_nonexistent_inventory_item(client):
    reset_inventory()

    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"


def test_add_inventory_item(client):
    reset_inventory()

    new_item = {
        "product_name": "Organic Soy Milk",
        "brand": "Alpro",
        "barcode": "0123456789014",
        "price": 480,
        "stock": 25,
        "ingredients_text": "Water, soybeans"
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 3
    assert data["product_name"] == "Organic Soy Milk"
    assert len(inventory) == 3


def test_update_inventory_item(client):
    reset_inventory()

    response = client.patch(
        "/inventory/1",
        json={
            "price": 475,
            "stock": 18
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 475
    assert data["stock"] == 18


def test_update_nonexistent_inventory_item(client):
    reset_inventory()

    response = client.patch(
        "/inventory/999",
        json={"price": 100}
    )

    assert response.status_code == 404


def test_delete_inventory_item(client):
    reset_inventory()

    response = client.delete("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Inventory item deleted successfully"
    assert len(inventory) == 1


def test_delete_nonexistent_inventory_item(client):
    reset_inventory()

    response = client.delete("/inventory/999")

    assert response.status_code == 404


def test_import_product_from_openfoodfacts(client):
    reset_inventory()

    fake_product = {
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0123456789012",
        "ingredients_text": "Filtered water, almonds, cane sugar"
    }

    with patch(
        "app.routes.search_product_by_barcode",
        return_value=fake_product
    ):
        response = client.post(
            "/inventory/import",
            json={
                "barcode": "0123456789012",
                "price": 450,
                "stock": 20
            }
        )

    assert response.status_code == 201

    data = response.get_json()

    assert data["product_name"] == "Organic Almond Milk"
    assert data["brand"] == "Silk"
    assert data["price"] == 450
    assert data["stock"] == 20
    assert len(inventory) == 3


def test_import_product_not_found(client):
    reset_inventory()

    with patch(
        "app.routes.search_product_by_barcode",
        return_value=None
    ):
        response = client.post(
            "/inventory/import",
            json={
                "barcode": "0000000000000",
                "price": 450,
                "stock": 20
            }
        )

    assert response.status_code == 404


def test_import_product_requires_barcode(client):
    reset_inventory()

    response = client.post(
        "/inventory/import",
        json={
            "price": 450,
            "stock": 20
        }
    )

    assert response.status_code == 400