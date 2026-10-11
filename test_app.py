import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_add_item(client):
    response = client.post('/inventory', json={
        "product_name": "Test Item",
        "price": 1.99,
        "stock": 10
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Item"