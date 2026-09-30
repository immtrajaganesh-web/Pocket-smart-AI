import os
os.environ['DATABASE_URL'] = 'sqlite:///./data/test.db'
os.environ['GEMINI_API_KEY'] = ''
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def login():
    email = 'test@example.com'
    r = client.post('/api/auth/register', json={'name': 'Test User', 'email': email, 'password': 'password123'})
    assert r.status_code in (201, 409)
    r = client.post('/api/auth/login', json={'email': email, 'password': 'password123'})
    assert r.status_code == 200
    return r.json()['access_token']

def test_health():
    assert client.get('/api/health').json()['status'] == 'ok'

def test_home():
    t = login()
    r = client.post(
        '/api/generate-home',
        headers={'Authorization': f'Bearer {t}'},
        json={
            'budget': 30000,
            'currency': 'INR',
            'rooms': ['Living Room'],
            'items': {'lights': 4},
            'style': 'modern',
            'priorities': ['lighting']
        }
    )
    assert r.status_code == 200
    assert r.json()['source_mode'] == 'fallback'

def test_party():
    t = login()
    r = client.post(
        '/api/generate-party',
        headers={'Authorization': f'Bearer {t}'},
        json={
            'budget': 20000,
            'currency': 'INR',
            'guests': 30,
            'event_type': 'birthday',
            'venue': 'indoor',
            'city': 'Chennai',
            'preferences': ['vegetarian']
        }
    )
    assert r.status_code == 200
    assert r.json()['source_mode'] == 'fallback'

def test_jewelry():
    t = login()
    r = client.post(
        '/api/generate-jewelry',
        headers={'Authorization': f'Bearer {t}'},
        data={
            'budget': 15000,
            'currency': 'INR',
            'occasion': 'wedding',
            'style': 'kundan',
            'metal': 'gold',
            'outfit_description': 'Emerald green silk saree'
        }
    )
    assert r.status_code == 200
    assert r.json()['source_mode'] == 'fallback'
    assert 'allocations' in r.json()
