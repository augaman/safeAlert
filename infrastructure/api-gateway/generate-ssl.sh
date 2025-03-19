#!/bin/bash

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Generate private key
openssl genrsa -out ssl/kong.key 2048

# Generate CSR (Certificate Signing Request)
openssl req -new -key ssl/kong.key -out ssl/kong.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=api.safealert.com"

# Generate self-signed certificate (for development)
openssl x509 -req -days 365 -in ssl/kong.csr -signkey ssl/kong.key -out ssl/kong.crt

# Set proper permissions
chmod 600 ssl/kong.key
chmod 644 ssl/kong.crt

echo "SSL certificates generated successfully!" 