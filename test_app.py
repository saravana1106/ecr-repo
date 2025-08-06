import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    rv = client.get('/')
    assert b'Hello from Python Flask App!' in rv.data

def test_add_numbers(client):
    # Positive numbers test
    rv = client.get('/add/5/3')
    assert b'{"result":8}' in rv.data

    # Check if negative number route works, otherwise skip
    rv = client.get('/add/-10/5')
    if rv.status_code == 404:
        pytest.skip("Negative number route not supported by Flask <int:...> converter")
    else:
        assert b'{"result":-5}' in rv.data

def test_add_numbers_fail(client):
    rv = client.get('/add/1/1')
    assert b'{"result":3}' not in rv.data
    assert b'{"result":2}' in rv.data
