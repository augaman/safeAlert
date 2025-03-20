# Messaging Service

A microservice responsible for facilitating inter-service communication by handling message dispatching and consumption. This service serves as a wrapper for integrating a messaging broker such as RabbitMQ or Apache Kafka.

## Features

- Message sending and status tracking
- Health check endpoint
- Stubbed message broker integration (ready for RabbitMQ/Kafka)
- JSON logging
- Docker support
- Comprehensive test coverage

## API Endpoints

### POST /messages/send

Send a new message.

**Request Body:**
```json
{
    "sender": "string",
    "recipient": "string",
    "content": "string",
    "message_type": "string",
    "priority": "LOW|MEDIUM|HIGH",
    "timestamp": "ISO8601 datetime (optional)"
}
```

**Response (201 Created):**
```json
{
    "id": "string",
    "sender": "string",
    "recipient": "string",
    "content": "string",
    "message_type": "string",
    "priority": "string",
    "timestamp": "ISO8601 datetime",
    "status": "SENT"
}
```

### GET /messages/health

Check the health of the messaging service.

**Response (200 OK):**
```json
{
    "status": "healthy"
}
```

### GET /messages/{message_id}/status

Get the status of a specific message.

**Response (200 OK):**
```json
{
    "status": "PENDING|SENT|FAILED",
    "error_message": "string (optional)"
}
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
flask run
```

## Docker

Build the image:
```bash
docker build -t messaging-service .
```

Run the container:
```bash
docker run -p 5000:5000 messaging-service
```

## Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Future Enhancements

1. Integrate with RabbitMQ:
   - Add connection pooling
   - Implement message persistence
   - Add exchange and queue management

2. Integrate with Apache Kafka:
   - Add topic management
   - Implement consumer groups
   - Add message partitioning

3. Add Message Features:
   - Message retry mechanism
   - Dead letter queue
   - Message validation rules
   - Message routing

4. Monitoring:
   - Add Prometheus metrics
   - Implement health checks for broker connection
   - Add message throughput monitoring

## Development

### Project Structure

```
messages/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   ├── schemas.py
│   └── messaging.py
├── tests/
│   ├── __init__.py
│   └── test_messaging.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### Adding New Features

1. Define new schemas in `schemas.py`
2. Add new routes in `routes.py`
3. Implement business logic in `messaging.py`
4. Add tests in `test_messaging.py`
5. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 