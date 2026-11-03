import pytest
from app import app, inventory


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ---- GET /inventory ----

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_item_found(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_item_not_found(client):
    response = client.get('/inventory/9999')
    assert response.status_code == 404


# ---- POST /inventory ----

def test_add_item(client):
    response = client.post('/inventory', json={
        "product_name": "Test Item",
        "price": 1.99,
        "stock": 10
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Item"
    assert data["price"] == 1.99
    assert data["stock"] == 10


def test_add_item_missing_name(client):
    response = client.post('/inventory', json={"price": 1.99})
    assert response.status_code == 400
    assert "error" in response.get_json()


# ---- PATCH /inventory/<id> ----

def test_update_item(client):
    add_res = client.post('/inventory', json={"product_name": "Update Me", "price": 5.0, "stock": 5})
    item_id = add_res.get_json()["id"]

    response = client.patch(f'/inventory/{item_id}', json={"price": 7.5})
    assert response.status_code == 200
    assert response.get_json()["price"] == 7.5


def test_update_item_not_found(client):
    response = client.patch('/inventory/9999', json={"price": 1.0})
    assert response.status_code == 404


# ---- DELETE /inventory/<id> ----

def test_delete_item(client):
    add_res = client.post('/inventory', json={"product_name": "Delete Me", "price": 2.0, "stock": 1})
    item_id = add_res.get_json()["id"]

    response = client.delete(f'/inventory/{item_id}')
    assert response.status_code == 200

    get_res = client.get(f'/inventory/{item_id}')
    assert get_res.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete('/inventory/9999')
    assert response.status_code == 404


# ---- External API routes ----

def test_external_product_bad_barcode(client):
    response = client.get('/external-product/000000000000')
    # either 404 (not found on OFF) or 502 (network blocked in CI) are acceptable
    assert response.status_code in (404, 502)


def test_import_external_product_bad_barcode(client):
    response = client.post('/external-product/000000000000/import', json={"price": 1.0, "stock": 1})
    assert response.status_code in (404, 502)


# ---- Helper routes ----

def test_search_inventory_missing_query(client):
    response = client.get('/inventory/search')
    assert response.status_code == 400


def test_search_inventory_found(client):
    client.post('/inventory', json={"product_name": "Searchable Widget", "price": 1.0, "stock": 1})
    response = client.get('/inventory/search', query_string={"q": "widget"})
    assert response.status_code == 200
    results = response.get_json()
    assert any("Widget" in r["product_name"] for r in results)


def test_low_stock(client):
    client.post('/inventory', json={"product_name": "Low Stock Item", "price": 1.0, "stock": 1})
    response = client.get('/inventory/low-stock', query_string={"threshold": 5})
    assert response.status_code == 200
    results = response.get_json()
    assert all(i["stock"] <= 5 for i in results)


def test_inventory_summary(client):
    response = client.get('/inventory/summary')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_items" in data
    assert "total_units" in data
    assert "total_value" in data