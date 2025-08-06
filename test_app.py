import pytest
from urllib.parse import quote
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    rv = client.get('/')
    assert rv.get_json() == {"message": "Hello from Python Flask App!"}

def test_add_numbers(client):
    rv = client.get('/add/1/1')
    assert rv.get_json() == {"result": 2}

    rv = client.get(f"/add/{quote(str(-10))}/5")  # handles negative value
    assert rv.get_json() == {"result": -5}

def test_add_numbers_fail(client):
    rv = client.get('/add/1/1')
    assert rv.get_json() != {"result": 3}
    assert rv.get_json() == {"result": 2}
