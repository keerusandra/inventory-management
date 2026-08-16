# Inventory Management System

A Flask-based REST API for managing inventory items. The application supports
CRUD operations and integrates with the OpenFoodFacts API to retrieve product
information using a barcode.

## Project Overview

This project was created as a summative lab to demonstrate:

- Flask REST API development
- CRUD operations
- External API integration
- Mock data storage using a Python list
- Automated testing with pytest
- Mocking external API responses
- Git and GitHub workflow

The inventory is currently stored in a Python list to simulate a database.

## Technologies Used

- Python
- Flask
- Requests
- Pytest
- unittest.mock
- OpenFoodFacts API
- Git and GitHub

## Project Structure

```text
inventory-management/
│
├── app/
│   ├── __init__.py
│   ├── inventory.py
│   ├── routes.py
│   └── openfoodfacts.py
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_openfoodfacts.py
│
├── run.py
├── requirements.txt
└── README.md

Installation
1. Clone the repository
git clone https://github.com/keerusandra/inventory-management

2. Enter the project directory
cd inventory-management

3. Create a virtual environment
python3 -m venv venv

4. Activate the virtual environment
On Linux/macOS:
source venv/bin/activate

5. Install dependencies
pip install -r requirements.txt

Running the Application

Start the Flask application with:

python run.py

The API will be available at:

http://127.0.0.1:5000
API Endpoints
Get all inventory
GET /inventory

Returns all inventory items.

Example:

curl http://127.0.0.1:5000/inventory

Get one inventory item
GET /inventory/<id>

Example:

curl http://127.0.0.1:5000/inventory/1
Add an inventory item
POST /inventory

Example:

{
    "product_name": "Organic Soy Milk",
    "brand": "Alpro",
    "barcode": "0123456789014",
    "price": 480,
    "stock": 25,
    "ingredients_text": "Water, soybeans"
}
Update an inventory item
PATCH /inventory/<id>

Example:
{
    "price": 475,
    "stock": 18
}

Delete an inventory item
DELETE /inventory/<id>

Example:

curl -X DELETE http://127.0.0.1:5000/inventory/1
OpenFoodFacts Integration

The application connects to the OpenFoodFacts API to retrieve product
information using a barcode.

Search for a product
GET /products/search?barcode=<barcode>

Example:

curl "http://127.0.0.1:5000/products/search?barcode=0123456789012"

The application can retrieve information such as:

Product name
Brand
Barcode
Ingredients
Import a product into inventory
POST /inventory/import

Example request:

{
    "barcode": "0123456789012",
    "price": 450,
    "stock": 20
}

The application retrieves the product information from OpenFoodFacts and
adds it to the inventory list.

Testing

Tests are written using pytest.

Run all tests:

pytest -v

The test suite covers:

Getting all inventory
Getting an individual inventory item
Handling nonexistent inventory items
Adding inventory
Updating inventory
Deleting inventory
OpenFoodFacts product searches
OpenFoodFacts product-not-found responses
OpenFoodFacts request failures
Importing products from OpenFoodFacts
Invalid import requests

External API calls are mocked using unittest.mock so that tests do not
depend on the availability of the OpenFoodFacts service.

Mock Database

The application currently uses a Python list as temporary storage instead of
a database.

Example:

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0123456789012",
        "price": 450.00,
        "stock": 20
    }
]

Each inventory item has a unique ID.

Error Handling

The API returns appropriate HTTP status codes for common errors.

Examples:

200 - Successful request
201 - Inventory item successfully created
400 - Invalid request
404 - Inventory item or product not found
503 - External API unavailable
Future Improvements

Planned improvements include:

Command-line interface (CLI)
CLI testing
Persistent database storage
Additional product search options
Improved validation
Authentication for administrative users

Author
Created as part of a Python Flask REST API summative lab.