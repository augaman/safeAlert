# Billing & Audit Service

A microservice responsible for handling invoice generation and audit logging. This service provides endpoints for retrieving invoices, recording audit logs, and monitoring system health.

## Features

- Invoice management with pagination and filtering
- Audit log recording
- Health check endpoint
- PostgreSQL database integration
- JSON logging
- Docker support
- Comprehensive test coverage

## API Endpoints

### GET /billing/invoices

Retrieve a list of invoices with pagination and filtering.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 10)
- `status` (optional): Filter by status (PENDING|PAID|OVERDUE)

**Response (200 OK):**
```json
{
    "items": [
        {
            "id": 1,
            "invoice_number": "INV-001",
            "amount": "100.00",
            "status": "PENDING",
            "created_at": "2024-03-19T20:00:00",
            "updated_at": "2024-03-19T20:00:00"
        }
    ],
    "total": 100,
    "page": 1,
    "size": 10,
    "pages": 10
}
```

### POST /billing/log

Record a new audit log entry.

**Request Body:**
```json
{
    "event_type": "string",
    "description": "string",
    "user_id": "string (optional)"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "event_type": "string",
    "description": "string",
    "user_id": "string",
    "timestamp": "2024-03-19T20:00:00"
}
```

### GET /billing/health

Check the health of the service.

**Response (200 OK):**
```json
{
    "status": "healthy",
    "database": "healthy",
    "timestamp": "2024-03-19T20:00:00"
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

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Run the service:
```bash
flask run
```

## Docker

Build the image:
```bash
docker build -t billing-service .
```

Run the container:
```bash
docker run -p 5000:5000 \
    -e DATABASE_URL=postgresql://user:password@host:5432/db \
    billing-service
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

## Database Schema

### Invoices Table
- `id`: Primary key
- `invoice_number`: Unique identifier
- `amount`: Decimal(10,2)
- `status`: Enum (PENDING|PAID|OVERDUE)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Audit Logs Table
- `id`: Primary key
- `event_type`: String(100)
- `description`: Text
- `user_id`: String(100)
- `timestamp`: Timestamp

## Development

### Project Structure

```
billing/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
├── migrations/
│   └── versions/
│       └── 001_initial.py
├── tests/
│   ├── __init__.py
│   └── test_billing.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### Adding New Features

1. Define new models in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Add routes in `routes.py`
4. Create database migrations
5. Add tests
6. Update documentation

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