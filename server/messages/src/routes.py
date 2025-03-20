"""Routes for the messaging service."""
from flask import Blueprint, request, jsonify
from .schemas import MessageCreate, MessageResponse, MessageStatus
from .messaging import MessagingHandler
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
messages_bp = Blueprint('messages', __name__)

# Initialize messaging handler
messaging_handler = MessagingHandler()


@messages_bp.route('/messages/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        is_healthy = messaging_handler.health_check()
        if is_healthy:
            return jsonify({"status": "healthy"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 503
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@messages_bp.route('/messages/send', methods=['POST'])
def send_message():
    """Send a message endpoint."""
    try:
        # Validate request data
        data = MessageCreate(**request.get_json())
        
        # Send message
        response = messaging_handler.send_message(data)
        
        logger.info(f"Message sent successfully: {response.id}")
        return jsonify(response.dict()), 201
        
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return jsonify({"error": str(e)}), 400


@messages_bp.route('/messages/<message_id>/status', methods=['GET'])
def get_message_status(message_id):
    """Get message status endpoint."""
    try:
        status = messaging_handler.get_message_status(message_id)
        if status is None:
            return jsonify({"error": "Message not found"}), 404
        
        return jsonify(status.dict()), 200
        
    except Exception as e:
        logger.error(f"Failed to get message status: {str(e)}")
        return jsonify({"error": str(e)}), 400 