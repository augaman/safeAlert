import pytest
from app import app, db, User
import os
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_health_check(client):
    response = client.get('/auth/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_register_success(client):
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post('/auth/register', json=data)
    assert response.status_code == 201
    assert 'user' in response.json
    assert response.json['user']['email'] == data['email']
    assert response.json['user']['first_name'] == data['first_name']
    assert response.json['user']['last_name'] == data['last_name']

def test_register_duplicate_email(client):
    # Register first user
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/auth/register', json=data)
    
    # Try to register with same email
    response = client.post('/auth/register', json=data)
    assert response.status_code == 400
    assert 'already registered' in response.json['error']

def test_login_success(client):
    # Register user first
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/auth/register', json=data)
    
    # Try to login
    login_data = {
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'user' in response.json

def test_login_invalid_credentials(client):
    login_data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 401
    assert 'Invalid credentials' in response.json['error']

def test_validate_token(client):
    # Register and login user
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/auth/register', json=data)
    
    login_data = {
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    login_response = client.post('/auth/login', json=login_data)
    token = login_response.json['access_token']
    
    # Validate token
    response = client.get('/auth/validate', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['valid'] == True
    assert 'user' in response.json

def test_validate_invalid_token(client):
    response = client.get('/auth/validate', headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 401 