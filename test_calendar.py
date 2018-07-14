import pytest

import main as calendar

@pytest.fixture
def client():
    calendar.app.config['TESTING'] = True
    client = calendar.app.test_client()
    yield client

def test_initial_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Click "Login to Eventbrite" below' in rv.data