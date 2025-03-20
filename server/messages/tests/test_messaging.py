"""Test module for messaging service."""
import pytest
from datetime import datetime
from src.app import create_app
from src.schemas import MessageCreate, MessageResponse, MessageStatus
from src.messaging import MessagingHandler


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def messaging_handler():
    """Create a test messaging handler."""
    return MessagingHandler()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/messages/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_send_message(client):
    """Test sending a message."""
    data = {
        'sender': 'test_sender',
        'recipient': 'test_recipient',
        'content': 'Test message content',
        'message_type': 'TEST',
        'priority': 'LOW'
    }
    
    response = client.post('/messages/send', json=data)
    assert response.status_code == 201
    
    result = response.json
    assert result['sender'] == data['sender']
    assert result['recipient'] == data['recipient']
    assert result['content'] == data['content']
    assert result['message_type'] == data['message_type']
    assert result['priority'] == data['priority']
    assert 'id' in result
    assert 'timestamp' in result
    assert result['status'] == 'SENT'


def test_send_message_invalid_data(client):
    """Test sending a message with invalid data."""
    data = {
        'sender': '',  # Empty sender
        'recipient': 'test_recipient',
        'content': 'Test message content',
        'message_type': 'TEST',
        'priority': 'INVALID'  # Invalid priority
    }
    
    response = client.post('/messages/send', json=data)
    assert response.status_code == 400


def test_get_message_status(client):
    """Test getting message status."""
    # First send a message
    data = {
        'sender': 'test_sender',
        'recipient': 'test_recipient',
        'content': 'Test message content',
        'message_type': 'TEST',
        'priority': 'LOW'
    }
    
    response = client.post('/messages/send', json=data)
    assert response.status_code == 201
    message_id = response.json['id']
    
    # Then get its status
    response = client.get(f'/messages/{message_id}/status')
    assert response.status_code == 200
    
    result = response.json
    assert result['status'] == 'SENT'


def test_get_message_status_not_found(client):
    """Test getting status of non-existent message."""
    response = client.get('/messages/nonexistent/status')
    assert response.status_code == 404


def test_messaging_handler_connection(messaging_handler):
    """Test messaging handler connection."""
    assert messaging_handler.connect() is True
    assert messaging_handler.is_connected is True
    assert messaging_handler.health_check() is True


def test_messaging_handler_disconnect(messaging_handler):
    """Test messaging handler disconnection."""
    messaging_handler.connect()
    messaging_handler.disconnect()
    assert messaging_handler.is_connected is False
    assert messaging_handler.health_check() is False


def test_messaging_handler_send_message(messaging_handler):
    """Test sending message through handler."""
    message = MessageCreate(
        sender='test_sender',
        recipient='test_recipient',
        content='Test message content',
        message_type='TEST',
        priority='LOW'
    )
    
    response = messaging_handler.send_message(message)
    assert isinstance(response, MessageResponse)
    assert response.sender == message.sender
    assert response.recipient == message.recipient
    assert response.content == message.content
    assert response.message_type == message.message_type
    assert response.priority == message.priority
    assert response.status == 'SENT'


def test_messaging_handler_get_status(messaging_handler):
    """Test getting message status through handler."""
    # First send a message
    message = MessageCreate(
        sender='test_sender',
        recipient='test_recipient',
        content='Test message content',
        message_type='TEST',
        priority='LOW'
    )
    
    response = messaging_handler.send_message(message)
    message_id = response.id
    
    # Then get its status
    status = messaging_handler.get_message_status(message_id)
    assert isinstance(status, MessageStatus)
    assert status.status == 'SENT' 