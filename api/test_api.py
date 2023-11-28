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