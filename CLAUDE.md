# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```bash
uv pip install -r requirements.txt -r requirements-dev.txt
```

**Run development server:**
```bash
uvicorn app.main:app --reload
```

**Lint with Ruff:**
```bash
ruff check .
ruff check . --fix
```

**Run tests:**
```bash
pytest -q
pytest tests/test_prompt_builder.py -v
```

**Docker build:**
```bash
docker build -t ai-draw-guess:latest .
```

**Docker Compose (development):**
```bash
docker-compose up -d
docker-compose logs -f
```

## Architecture

This is an AI-powered "Draw and Guess" (你画我猜) web application where users draw on a canvas and AI attempts to guess what they've drawn.

**Tech Stack:**
- Backend: FastAPI + Uvicorn (Python)
- Frontend: HTML5 Canvas + vanilla JavaScript
- AI: Baishan AI API (DeepSeek-R1-0528 model)
- Linting: Ruff, Testing: pytest

**Directory Structure:**
- `app/main.py` - FastAPI application entry point with endpoints:
  - `GET /` - Serves the frontend
  - `GET /api/health` - Health check
  - `POST /api/guess` - Accept drawing strokes and get AI guess
- `app/config.py` - Environment configuration (BAISHAN_API_KEY, model settings)
- `app/ai_client.py` - Baishan API client with retry logic
- `app/prompt_builder.py` - Converts drawing strokes to text prompts for AI
- `app/schemas.py` - Pydantic request/response schemas
- `app/templates/index.html` - Frontend drawing canvas
- `tests/` - Test suite (currently tests prompt builder)

**Key Design Points:**
- Drawing data is sent as an array of strokes (each stroke is array of points {x, y, timestamp)
- AI responses are in Chinese
- Retry logic for 503 and network errors from the AI API
- Environment variables configured via `.env` file (not committed to git)

## Environment Variables

Required:
- `BAISHAN_API_KEY` - Baishan AI API key

Optional:
- `BAISHAN_MODEL` - Model name (default: deepseek-v3-250515)
- `BAISHAN_BASE_URL` - API base URL (default: https://api.edgefn.net/v1)

## CI/CD

GitHub Actions CI runs on every commit/PR:
- Ruff linting
- pytest tests

See `.github/workflows/ci.yml
