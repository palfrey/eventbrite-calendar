import pytest
import os

def default_env_key(mp, key, value):
    if key not in os.environ:
        mp.setitem(os.environ, key, value)

@pytest.fixture
def client(monkeypatch):
    default_env_key(monkeypatch, "EVENTBRITE_API_KEY", "foo")
    default_env_key(monkeypatch, "EVENTBRITE_OAUTH_SECRET", "wibble")
    default_env_key(monkeypatch, "EVENTBRITE_OAUTH_CODE", "bar")
    import main as calendar
    calendar.app.config['TESTING'] = True
    client = calendar.app.test_client()
    yield client

def test_initial_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Click "Login to Eventbrite" below' in rv.data

def test_oauth_redirect(client):
    rv = client.get('/?code=bar')
    assert rv.status_code == 302
    assert rv.headers["location"] == "http://localhost/oauth/bar"

def test_oauth(client):
    rv = client.get(f'/oauth/{os.environ["EVENTBRITE_OAUTH_CODE"]}')
    assert rv.status_code == 302