import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'User Management System' in resp.data

def test_create_and_get_user(client):
    # Create user
    resp = client.post('/users', json={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'testpass'
    })
    assert resp.status_code == 201
    # Get all users
    resp = client.get('/users')
    assert resp.status_code == 200
    users = resp.get_json()
    assert any(u['email'] == 'testuser@example.com' for u in users)

def test_create_user_invalid_email(client):
    resp = client.post('/users', json={
        'name': 'Bad Email',
        'email': 'notanemail',
        'password': 'testpass'
    })
    assert resp.status_code == 400

def test_login_success_and_fail(client):
    # Create user
    client.post('/users', json={
        'name': 'Login User',
        'email': 'login@example.com',
        'password': 'secret'
    })
    # Successful login
    resp = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'secret'
    })
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'success'
    # Failed login
    resp = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'wrongpass'
    })
    assert resp.status_code == 401
    assert resp.get_json()['status'] == 'failed'

def test_update_and_delete_user(client):
    # Create user
    resp = client.post('/users', json={
        'name': 'To Update',
        'email': 'update@example.com',
        'password': 'pw'
    })
    users = client.get('/users').get_json()
    user = next(u for u in users if u['email'] == 'update@example.com')
    user_id = user['id']
    # Update
    resp = client.put(f'/user/{user_id}', json={
        'name': 'Updated',
        'email': 'updated@example.com'
    })
    assert resp.status_code == 200
    # Delete
    resp = client.delete(f'/user/{user_id}')
    assert resp.status_code == 200
    # Confirm deletion
    resp = client.get(f'/user/{user_id}')
    assert resp.status_code == 404
