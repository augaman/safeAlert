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
├── docs/             # Project documentation
├── scripts/          # Utility scripts
└── backups/          # Local backups (gitignored)
```

## Version Control Guidelines

### Branch Protection
- `main`: Production branch, protected from direct pushes
- `develop`: Development branch, requires pull request review
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation
- `hotfix/*`: Emergency fixes

### Commit Guidelines
1. Use conventional commits format:
   ```
   type(scope): description
   
   [optional body]
   [optional footer]
   ```
   Types: feat, fix, docs, style, refactor, test, chore

2. Always include a clear description of changes
3. Reference issues/tickets in commit messages when applicable

### Backup Procedures
1. Local Backups:
   - Run `.\scripts\backup.ps1` to create a timestamped backup
   - Backups are stored in the `backups/` directory
   - Last 5 backups are retained automatically

2. Remote Backup:
   - All branches are automatically backed up to GitHub
   - Critical branches (main, develop) require pull request review
   - Tags are used for release versions

### Safe Development Practices
1. Never work directly on main or develop branches
2. Create feature branches for all changes:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```
3. Regular commits and pushes:
   ```bash
   git add .
   git commit -m "feat(component): description"
   git push origin feature/your-feature-name
   ```
4. Create pull requests for review before merging

### Recovery Procedures
1. To revert a commit:
   ```bash
   git revert <commit-hash>
   ```
2. To restore from backup:
   - Unzip the desired backup from `backups/`
   - Copy files as needed

3. To switch to a previous state:
   ```bash
   git checkout <commit-hash>
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