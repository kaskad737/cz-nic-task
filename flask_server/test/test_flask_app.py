import sys
sys.path.append('/home/apti/cz-nic-test-task/flask_server/')
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_file_metadata_endpoint(client):
    response = client.get('/file/1/stat/')
    assert response.status_code == 200
    assert response.json == {'create_datetime': 1702031346.009876, 'mimetype': 'text/plain', 'name': 'test_file_1', 'size': 1005}

def test_read_file_endpoint(client):
    response = client.get('/file/1/read/')
    assert response.status_code == 200
    assert response.text[:26] == 'Lorem ipsum dolor sit amet'

def test_file_metadata_endpoint_file_not_found(client):
    response = client.get('/file/5/stat/')
    assert response.status_code == 404
    assert response.text == 'File not found. Error code 404'

def test_read_file_endpoint_file_not_found(client):
    response = client.get('/file/5/read/')
    assert response.status_code == 404
    print(response.text)
    assert response.text == 'File not found. Error code 404'