import pytest
from api import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    return app.test_client()

def test_tischreservierung(app):
    route = "/"
    response = app.get(route)
    assert response.status_code == 200
    assert b"<h1>Tischreservierung</h1>" in response.data

# def test_reservations__all(app):
#     route = "/api/v1/reservations" 
#     expected =b'{"pin":1331,"reservierungsnummer":1,"storniert":"False","tischnummer":1,"zeitpunkt":"2022-02-02 17:30:00"}'

#     response = app.get(route)
#     assert response.status_code == 200
#     assert expected in response.data

def test_reservations__all(app):
    route = "/api/v1/reservations" 
    expected =b'pin":'

    response = app.get(route)
    assert response.status_code == 200
    assert expected in response.data