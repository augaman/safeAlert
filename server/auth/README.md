# SafeAlert Authentication Service

This service handles user authentication and authorization for the SafeAlert platform.

## Features

- User registration and login
- JWT token generation and validation
- Password hashing with bcrypt
- Health check endpoint
- Database migrations with Alembic
- Comprehensive test suite

## API Endpoints

### Health Check
- `GET /auth/health`
  - Returns service health status
  - No authentication required

### User Registration
- `POST /auth/register`
  - Register a new user
  - Request body:
    ```json
    {
      "email": "user@example.com",
      "password": "securepassword",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```
  - Returns: User object (excluding password)

### User Login
- `POST /auth/login`
  - Authenticate user and get JWT token
  - Request body:
    ```json
    {
      "email": "user@example.com",
      "password": "securepassword"
    }
    ```
  - Returns: JWT token and user object

### Token Validation
- `GET /auth/validate`
  - Validate JWT token
  - Requires Authorization header: `Bearer <token>`
  - Returns: Token validity and user object

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

4. Initialize the database:
   ```bash
   flask db upgrade
   ```

5. Run the service:
   ```bash
   # Development
   flask run
   
   # Production
   gunicorn app:app
   ```

## Testing

Run the test suite:
```bash
pytest
```

## Docker

Build the image:
```bash
docker build -t safealert-auth .
```

Run the container:
```bash
docker run -p 8000:8000 safealert-auth
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `FLASK_ENV`: Environment (development/production)

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens expire after 1 hour
- All endpoints except health check require authentication
- Input validation using Pydantic
- CORS enabled for specified origins

## Development

1. Create a new branch for your feature
2. Make your changes
3. Write/update tests
4. Run the test suite
5. Submit a pull request

## License

Proprietary - All rights reserved 