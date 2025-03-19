# SafeAlert Emergency Response System

A comprehensive emergency response system comprising mobile clients, web dashboard, and intervention applications.

## Project Structure

```
safeAlert/
├── client-mobile/      # Mobile app for emergency reporting
├── dispatch-web/       # Web dashboard for emergency dispatch
├── intervention-mobile/# Mobile app for first responders
├── server/            # Backend microservices
├── infrastructure/    # Infrastructure as Code (Docker, K8s)
└── docs/             # Project documentation
```

## Development Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- Docker
- Kubernetes (for deployment)
- Git

### Getting Started

1. Clone the repository:
```bash
git clone https://github.com/your-org/safeAlert.git
cd safeAlert
```

2. Install dependencies for each component:
```bash
# Mobile client
cd client-mobile
npm install

# Web dashboard
cd ../dispatch-web
npm install

# Intervention app
cd ../intervention-mobile
npm install

# Backend services
cd ../server
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Development Guidelines

### Branching Strategy
We follow the GitFlow branching strategy:
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation
- `hotfix/*`: Emergency fixes

### Commit Guidelines
- Use conventional commits format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat(auth): implement JWT authentication`

### Code Style
- JavaScript/TypeScript: ESLint + Prettier
- Python: PEP8 + Black
- All code must pass linting and tests before merging

## Testing
- Unit tests required for all new features
- Integration tests for critical paths
- E2E tests for user flows

## Documentation
- API documentation in `/docs/api`
- Architecture diagrams in `/docs/architecture`
- Deployment guides in `/docs/deployment`

## License
[Your License Here] 