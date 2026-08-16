from unittest.mock import Mock, patch

import requests

from app.openfoodfacts import search_product_by_barcode


def test_search_product_by_barcode():
    fake_response = Mock()

    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar"
        }
    }

    with patch(
        "app.openfoodfacts.requests.get",
        return_value=fake_response
    ):
        product = search_product_by_barcode("0123456789012")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["barcode"] == "0123456789012"


def test_product_not_found():
    fake_response = Mock()

    fake_response.json.return_value = {
        "status": 0
    }

    with patch(
        "app.openfoodfacts.requests.get",
        return_value=fake_response
    ):
        product = search_product_by_barcode("0000000000000")

    assert product is None


def test_openfoodfacts_request_failure():
    with patch(
        "app.openfoodfacts.requests.get",
        side_effect=requests.RequestException
    ):
        try:
            search_product_by_barcode("0123456789012")
        except requests.RequestException:
            assert True