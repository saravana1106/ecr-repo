import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    rv = client.get('/')
    # Check JSON directly instead of matching raw bytes
    json_data = rv.get_json()
    assert json_data == {"message": "Hello from Python Flask App!"}

@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 8),
    (-10, 5, -5),
    (1, 1, 2),  # fixed expected value
])
def test_add_numbers(client, a, b, expected):
    rv = client.get(f'/add/{a}/{b}')
    assert rv.status_code == 200
    assert rv.get_json() == {"result": expected}

def test_add_numbers_fail(client):
    rv = client.get('/add/1/1')
    # Designed to pass: result is 2, so should not equal 3
    assert rv.get_json() != {"result": 3}
    assert rv.get_json() == {"result": 2}
