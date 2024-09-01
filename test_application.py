import pytest
from application import application

@pytest.fixture
def client():
    application.debug=True
    with application.test_client() as client:
        yield client

def test_hello(client):
    response=client.get('/')
    assert response.data==b'Continuous Delivery Demo'
    assert response.status_code==200

def test_echo(client):
    response=client.get('/echo/Yassmine')
    assert response.json=={"new-name": "Yassmine"}
    assert response.status_code==200