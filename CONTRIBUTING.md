# Contributing to BRAINBLUE URBAIN

Thank you for your interest in contributing to BRAINBLUE URBAIN! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct. In short:
- Use inclusive language
- Be respectful of differing opinions
- Accept constructive criticism gracefully
- Focus on what is best for the community

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git
- PostgreSQL 13+ (if running locally)
- Redis (if running locally)

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/BRAINBLUE.git
   cd BRAINBLUE
   ```

2. **Create a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 pylint
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Run with Docker Compose:**
   ```bash
   make setup  # Build, start services, run migrations
   ```

6. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - PgAdmin: http://localhost:5050 (dev only)

## Development Workflow

### Creating a Feature Branch

1. **Update main branch:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Code Style & Format

We follow PEP 8 guidelines with some customizations:

- **Python Code:**
  ```bash
  make format  # Automatically format code using Black and isort
  make lint    # Run linters to check code quality
  ```

- **Line Length:** 100 characters (Black default)
- **Imports:** Sorted with `isort`
- **Code Formatting:** Use `black` for consistent style

### Commit Messages

Follow the Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build, dependency, or tooling changes

**Examples:**
```
feat(maps): add real-time geolocation tracking

fix(api): resolve water level prediction timeout
docs(README): update installation instructions
```

### Writing Tests

Tests are crucial for maintaining code quality:

```python
# tests/test_api.py
import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
```

Run tests:
```bash
make test               # Run all tests
make test-coverage      # Run with coverage report
```

**Coverage target:** Aim for >80% code coverage for new features.

### Documentation

- Update docstrings in code using Google style:
  ```python
  def predict_water_level(network_id: str) -> dict:
      """
      Predict water level for a given network.
      
      Args:
          network_id: The unique identifier of the water network
          
      Returns:
          A dictionary containing prediction data and confidence
          
      Raises:
          ValueError: If network_id is invalid
      """
  ```

- Update README.md if adding new features
- Add inline comments for complex logic
- Keep API documentation updated

## Pull Request Process

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request on GitHub:**
   - Use a descriptive title and description
   - Reference related issues (closes #123)
   - Ensure all CI checks pass

3. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Related Issues
   Closes #123
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Changes Made
   - Change 1
   - Change 2
   
   ## Testing
   - [ ] Unit tests added
   - [ ] Integration tests passed
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guide
   - [ ] Self-review completed
   - [ ] Comments added for complex sections
   - [ ] Documentation updated
   - [ ] Tests pass locally
   ```

4. **Code Review:**
   - Address reviewer feedback promptly
   - Request changes if needed
   - Maintain respectful communication

### Merging

PR will be merged when:
- ✅ All CI checks pass
- ✅ At least one approval from maintainers
- ✅ All conversations resolved
- ✅ Code follows guidelines

## Reporting Bugs

Found a bug? Report it on GitHub Issues:

1. **Check existing issues** to avoid duplicates
2. **Include:**
   - Bug description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Python version, etc.)
   - Error logs/screenshots

3. **Use this template:**
   ```markdown
   ## Bug Description
   Brief description of the bug
   
   ## Steps to Reproduce
   1. Step 1
   2. Step 2
   3. ...
   
   ## Expected Behavior
   What should happen
   
   ## Actual Behavior
   What actually happened
   
   ## Environment
   - OS: [e.g., Windows 10]
   - Python: [e.g., 3.10]
   - Docker: [yes/no]
   
   ## Logs
   ```
   paste error logs here
   ```
   ```

## Feature Requests

Have an idea? Suggest it on GitHub Issues:

1. Use descriptive title
2. Explain use case and benefits
3. Provide examples or mockups if possible
4. Check if similar features exist

## Project Structure

```
BRAINBLUE/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config/             # Configuration files
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   └── database/           # Migrations and seeds
├── frontend/
│   └── index.html          # Main frontend file
├── tests/                  # Test suite
├── docs/                   # Documentation
├── docker-compose.yml      # Docker configuration
├── Dockerfile              # Flask container
├── Makefile                # Development commands
└── README.md               # Project documentation
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guidelines.

## Questions?

- 📧 Email: contact@brainblue.sn
- 💬 GitHub Discussions: [Project Discussions](https://github.com/yourusername/BRAINBLUE/discussions)
- 🐛 Report Issues: [GitHub Issues](https://github.com/yourusername/BRAINBLUE/issues)

## Additional Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

## License

By contributing to BRAINBLUE URBAIN, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to making BRAINBLUE URBAIN better! 🚀**
