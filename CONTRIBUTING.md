# Contributing to Sentinel-X

Thank you for your interest in contributing to Sentinel-X — an open-source AI Cognitive Safety OS for industrial environments. We welcome contributions of all kinds, from bug fixes and documentation improvements to new features and research collaborations.

Please read this guide carefully before opening a pull request.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Branch Strategy](#branch-strategy)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Security Vulnerabilities](#security-vulnerabilities)

---

## Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards. Please report unacceptable behavior to the maintainers.

---

## Ways to Contribute

| Type | Description |
|---|---|
| 🐛 **Bug Fixes** | Fix issues reported in GitHub Issues |
| 📄 **Documentation** | Improve README, docs/, folder READMEs |
| 🧪 **Tests** | Add pytest cases for backend or browser QA tests |
| 🌐 **Frontend** | Improve dashboard panels, add Three.js features |
| 🐍 **Backend** | Implement real database queries, WebSocket streaming |
| 🤖 **AI/ML** | Improve YOLOv11 model, integrate ONNX runtime |
| 🔧 **DevOps** | Improve CI pipeline, Docker images, K8s configs |
| 🔬 **Research** | Validate Digital DNA Fatigue Coefficient™ model |

---

## Development Setup

### Prerequisites

- **Git** ≥ 2.40
- **Python** ≥ 3.11 (for backend)
- **Modern browser** with WebGL support (for frontend)
- **Docker** ≥ 24.0 (for full stack)
- **PowerShell** (Windows, for dev server)

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/sentinel-x.git
cd sentinel-x

# Add upstream remote
git remote add upstream https://github.com/jaganbala2007/sentinel-x.git
```

### 2. Frontend Development

```powershell
# Start the local HTTP server
cd frontend/server
powershell -ExecutionPolicy Bypass -File dev-server.ps1

# Open http://localhost:8000 in your browser
```

### 3. Backend Development

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Edit .env with your local values

# Start development server (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# API docs: http://localhost:8080/docs
```

### 4. Full Stack with Docker

```bash
# Build and start all services
docker-compose -f deployment/docker-compose.yml up -d

# Check service health
docker-compose -f deployment/docker-compose.yml ps

# Tail logs
docker-compose -f deployment/docker-compose.yml logs -f
```

---

## Branch Strategy

We follow **GitHub Flow**:

```
main        — Production-stable releases only. Protected branch.
develop     — Integration branch for the next release.
feat/*      — New features (e.g., feat/onnx-inference)
fix/*       — Bug fixes (e.g., fix/otp-timer-reset)
docs/*      — Documentation updates (e.g., docs/improve-api-reference)
refactor/*  — Code refactoring without behavior change
chore/*     — Maintenance tasks (e.g., chore/update-dependencies)
```

**Never push directly to `main`.** All changes go through pull requests.

---

## Commit Message Convention

This project uses **Conventional Commits** for automated changelog generation:

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

### Types

| Type | When to Use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code restructure without behavior change |
| `test` | Adding or fixing tests |
| `chore` | Dependency updates, build config |
| `perf` | Performance improvement |
| `ci` | CI/CD pipeline changes |

### Examples

```bash
git commit -m "feat(vision): add YOLOv11 helmet color classification"
git commit -m "fix(auth): reset OTP countdown on resend button click"
git commit -m "docs(backend): add API authentication guide"
git commit -m "chore: upgrade fastapi to 0.115.0"
git commit -m "perf(3d-twin): reduce particle count to improve GPU frame rate"
```

---

## Pull Request Process

1. **Branch from `develop`** — never from `main`
2. **Keep PRs focused** — one feature or fix per PR
3. **Update documentation** — if your change affects behavior
4. **Ensure CI passes** — all 6 CI jobs must be green
5. **Write/update tests** — new backend endpoints must have tests
6. **Fill out the PR template** — don't skip sections
7. **Request a review** — tag `@jaganbala2007` for review

### PR Checklist (auto-populated from template)

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] New tests added for changed functionality
- [ ] Documentation updated
- [ ] CI pipeline passes
- [ ] No secrets or credentials committed

---

## Code Style Guidelines

### Python (Backend)

- **Formatter**: `ruff format` (Black-compatible)
- **Linter**: `ruff check`
- **Type hints**: Required on all public functions
- **Docstrings**: Google-style on all modules, classes, and public functions
- **Line length**: 100 characters

```bash
# Run formatter
ruff format backend/app/

# Run linter
ruff check backend/app/
```

### JavaScript (Frontend)

- Use `const` and `let` — never `var`
- Descriptive function and variable names
- Comment all major logic blocks
- Avoid global state where possible

### HTML

- Semantic HTML5 elements
- Unique `id` attributes on all interactive elements
- `aria-label` on icon-only buttons

---

## Testing Requirements

### Backend

All new API endpoints must have corresponding `pytest` tests in `/tests/`:

```python
# Example test structure
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_active_alerts():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/alerts/active")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
```

### Frontend

Add browser-side assertions in `frontend/src/test-suite.html`.

---

## Documentation Standards

- Every new file must have a **module-level docstring** (Python) or **comment header** (HTML/JS)
- Every new folder must have a **README.md** explaining its purpose
- Every new API endpoint must be documented in **`docs/api_specs.json`**
- Architecture changes must update **`docs/architecture.md`**

---

## Reporting Bugs

Use the [Bug Report template](https://github.com/jaganbala2007/sentinel-x/issues/new?template=bug_report.md).

Include:
- Browser/OS version
- Steps to reproduce
- Expected vs actual behavior
- Console error output (if applicable)

---

## Requesting Features

Use the [Feature Request template](https://github.com/jaganbala2007/sentinel-x/issues/new?template=feature_request.md).

---

## Security Vulnerabilities

**Do NOT open a public GitHub issue for security vulnerabilities.**  
Please read our [Security Policy](SECURITY.md) and report privately.

---

*Thank you for helping make industrial workplaces safer! 🛡️*
