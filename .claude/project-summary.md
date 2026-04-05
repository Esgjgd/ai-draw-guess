# AI Draw & Guess Project Summary

## 1. Project Type
This is an AI-powered "Draw and Guess" web application where users draw on a canvas and an AI model attempts to guess what they've drawn.

## 2. High-Level Architecture & Structure
The project follows a modern, lightweight architecture with:
- **FastAPI backend**: Handles API requests and AI integration
- **HTML5 Canvas frontend**: Provides drawing interface
- **Baishan AI API**: Analyzes drawing strokes to make guesses

### Key Components:
1. **Web Server**: Uvicorn ASGI server serving FastAPI app
2. **API Endpoints**:
   - `GET /` - Serves drawing interface
   - `GET /api/health` - Health check
   - `POST /api/guess` - Accepts stroke data, returns AI guess
3. **AI Integration**: Uses Baishan AI API with DeepSeek-R1-0528 model

## 3. Technology Stack
- **Python 3.10+** - Core language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **HTTPX** - Async HTTP client
- **Pydantic** - Data validation
- **Ruff** - Linting/formatter
- **Pytest** - Testing
- **Docker** - Containerization

## 4. Project Structure
```
ai-draw-guess/
├── app/                      # Main application
│   ├── main.py               # FastAPI endpoints
│   ├── config.py             # Configuration
│   ├── ai_client.py          # AI API client
│   ├── prompt_builder.py     # Prompt engineering
│   ├── schemas.py            # Data models
│   └── templates/
│       └── index.html        # Frontend
├── tests/                    # Test suite
│   └── test_prompt_builder.py
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline
├── pyproject.toml           # Project config
├── requirements.txt          # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── docker-compose.yml       # Docker config
└── Dockerfile               # Build instructions
```

## 5. Build/Lint/Test Commands
```bash
# Install dependencies
uv pip install -r requirements.txt -r requirements-dev.txt

# Run development server
uvicorn app.main:app --reload

# Lint with Ruff
ruff check .

# Run tests with Pytest
pytest -q
```

## 6. Configuration Files
- **pyproject.toml**: Project metadata, Ruff config, pytest settings
- **requirements.txt**: fastapi, uvicorn, httpx, python-dotenv, jinja2
- **requirements-dev.txt**: pytest, pytest-asyncio, ruff
- **.env.example**: Example environment variables (API key required)
- **docker-compose.yml**: Local development containerization

## 7. Getting Started
```bash
# 1. Configure environment variables
cp .env.example .env
# Edit .env file and add BAISHAN_API_KEY

# 2. Run with Docker Compose
docker-compose up -d

# 3. Visit http://127.0.0.1:8000
```

## 8. Features
- Browser-based drawing canvas with mouse/touch support
- AI guesses based on drawing strokes
- Basic canvas controls (clear, submit)
- Health check endpoint for monitoring

## 9. CI/CD Pipeline
GitHub Actions workflow runs on every push/pull request:
1. Lints with Ruff
2. Runs unit tests
3. Builds and tests Docker image

