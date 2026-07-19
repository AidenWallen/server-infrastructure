# SysHelper

An AI-powered gateway for server management and operations.

## Architecture
- **API Gateway**: FastAPI-based service with versioned routers (`/server`, `/chat`).
- **Security**: Mandatory `X-API-KEY` header via middleware; protected routes exclude health docs.
- **Database**: MongoDB (async) for persistent server state and logs; managed via the `ServerRepository` layer (service-layer pattern).
- **Service Layer**: Business logic lives in `app/services/` (e.g., `ServerService`) for clean separation and testability.
- **Monitoring**: `/health` endpoint, structured logging (`app.core.logger`).
- **Deployment**: Containerized via Docker Compose (includes MongoDB).

## Prerequisites
- Docker & Docker Compose installed.
- Python 3.11+ (for local development).

## Environment Configuration
Create a `.env` file in the project root. For local testing:
```env
# Database URL – injected by Docker Compose; override locally if needed
MONGO_URL=mongodb://mongo:27017

# AI backend
OLLAMA_URL=http://your-ollama-host:11434/api/generate
MODEL=your-model-name

# Secret used for request authentication (never commit real keys)
API_KEY=your-secure-api-key   # Use `test-key` for local pytest runs
```

## Getting Started
```bash
docker-compose up -d --build
```

### Verify
```bash
curl http://localhost:8000/health
# Expected output: {"status":"healthy","service":"sys-helper"}
```

## API Usage
All endpoints (except `/health`, `/docs`, `/openapi.json`) require the `X-API-KEY` header.

### Example: `/server` endpoint (GET)
```bash
curl -X GET http://localhost:8000/server/ \
     -H "X-API-KEY: your-secure-api-key"
```

### Example: `/chat` endpoint (POST)
```bash
curl -X POST http://localhost:8000/chat \
     -H "X-API-KEY: your-secure-api-key" \
     -H "Content-Type: application/json" \
     -d '{"message": "Check system status"}'
# Response: {"response": "..."}
```

## Running Tests
```bash
# Install test dependencies
pip install -r requirements.txt -r requirements-dev.txt
# Run the test suite
pytest -v
```