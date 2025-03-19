#!/bin/bash

# Create main directories
mkdir -p client-mobile/src
mkdir -p dispatch-web/src
mkdir -p intervention-mobile/src
mkdir -p server/src
mkdir -p infrastructure/{docker,k8s,terraform}
mkdir -p docs/{api,architecture,deployment}

# Initialize client-mobile (React Native)
cd client-mobile
npm init -y
npm install --save-dev @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint prettier jest @testing-library/react-native
cat > .eslintrc.js << EOL
module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  rules: {
    'react/react-in-jsx-scope': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
EOL

# Initialize dispatch-web (React)
cd ../dispatch-web
npm init -y
npm install --save-dev @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint prettier jest @testing-library/react
cp ../client-mobile/.eslintrc.js .

# Initialize intervention-mobile (React Native)
cd ../intervention-mobile
npm init -y
npm install --save-dev @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint prettier jest @testing-library/react-native
cp ../client-mobile/.eslintrc.js .

# Initialize server (Python)
cd ../server
python -m venv venv
echo "flask==2.0.1" > requirements.txt
echo "pytest==6.2.5" >> requirements.txt
echo "black==21.7b0" >> requirements.txt
echo "flake8==3.9.2" >> requirements.txt
echo "mypy==0.910" >> requirements.txt
cat > setup.cfg << EOL
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = .git,__pycache__,build,dist

[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
EOL

# Initialize infrastructure
cd ../infrastructure
cat > docker/docker-compose.yml << EOL
version: '3.8'

services:
  api:
    build: 
      context: ../server
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - FLASK_APP=src/app.py

  frontend:
    build:
      context: ../dispatch-web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api
EOL

# Create initial documentation
cd ../docs
cat > architecture/system-overview.md << EOL
# System Architecture Overview

## Components

1. Mobile Client App
   - Emergency reporting interface
   - Location tracking
   - Push notifications

2. Web Dashboard
   - Emergency dispatch interface
   - Real-time monitoring
   - Resource management

3. Intervention Mobile App
   - First responder interface
   - Navigation assistance
   - Emergency details view

4. Backend Services
   - Authentication service
   - Emergency management service
   - Location service
   - Notification service

## Technology Stack

- Frontend: React/React Native
- Backend: Python/Flask
- Database: PostgreSQL
- Message Queue: Redis
- Infrastructure: Docker, Kubernetes
EOL

# Initialize Git repository
cd ..
git init
git add .
git commit -m "Initial project setup"

echo "Project structure initialized successfully!" 