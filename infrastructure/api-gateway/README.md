# SafeAlert API Gateway Configuration

This directory contains the configuration for the SafeAlert API Gateway using Kong.

## Features

- TLS 1.3 Enforcement
- JWT Authentication
- Rate Limiting
- CORS Support
- Service Routing
- Health Checks

## Services

The API Gateway routes requests to the following microservices:

1. Authentication Service (`/auth`)
   - Rate limit: 60 requests per minute
   - JWT validation required
   - CORS enabled

2. Alert Management Service (`/alerts`)
   - Rate limit: 120 requests per minute
   - JWT validation required
   - CORS enabled

3. Messaging Service (`/messages`)
   - Rate limit: 180 requests per minute
   - JWT validation required
   - CORS enabled

4. Billing & Audit Service (`/billing`)
   - Rate limit: 60 requests per minute
   - JWT validation required
   - CORS enabled

## Setup Instructions

1. Generate SSL certificates:
   ```bash
   chmod +x generate-ssl.sh
   ./generate-ssl.sh
   ```

2. Start the API Gateway:
   ```bash
   docker-compose up -d
   ```

3. Verify the setup:
   ```bash
   curl -i https://localhost:8443/auth/health
   ```

## Configuration Files

- `kong-declarative-config.yaml`: Main Kong configuration
- `docker-compose.yml`: Docker services configuration
- `generate-ssl.sh`: SSL certificate generation script

## Security Features

### TLS 1.3
- All traffic is encrypted using TLS 1.3
- Self-signed certificates for development
- Production certificates should be obtained from a trusted CA

### JWT Authentication
- Validates JWT tokens in Authorization header
- Verifies token expiration
- Maximum token lifetime: 24 hours

### Rate Limiting
- Per-service rate limits
- Local policy for better performance
- Rate limit headers exposed to clients

### CORS
- Configurable origins
- Standard HTTP methods allowed
- Credentials support
- Preflight caching

## Monitoring

- Access logs: stdout
- Error logs: stderr
- Health checks for all services
- Kong Admin API available on port 8001

## Development

To modify the configuration:

1. Edit `kong-declarative-config.yaml`
2. Restart Kong:
   ```bash
   docker-compose restart kong
   ```

## Production Considerations

1. Replace self-signed certificates with proper CA-signed certificates
2. Configure proper CORS origins
3. Adjust rate limits based on service requirements
4. Set up proper monitoring and alerting
5. Configure backup for Kong database 