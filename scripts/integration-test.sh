#!/bin/bash

# Exit on error
set -e

echo "Starting integration tests..."

# Start test environment
echo "Starting test environment..."
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run API tests
echo "Running API tests..."
npm run test:api

# Run WebSocket tests
echo "Running WebSocket tests..."
npm run test:websocket

# Run end-to-end tests
echo "Running end-to-end tests..."
npm run test:e2e

# Run performance tests
echo "Running performance tests..."
npm run test:performance

# Check test results
if [ $? -eq 0 ]; then
  echo "All tests passed successfully!"
else
  echo "Tests failed. Check the logs for details."
  exit 1
fi

# Clean up
echo "Cleaning up test environment..."
docker-compose -f docker-compose.test.yml down

echo "Integration tests completed." 