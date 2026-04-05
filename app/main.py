from __future__ import annotations

import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.ai_client import BaishanAIClient
from app.config import get_settings
from app.prompt_builder import build_guess_prompt
from app.schemas import GuessRequest, GuessResponse

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# Global client instance - reused across requests for connection pooling
_ai_client: BaishanAIClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared resources on startup and cleanup on shutdown."""
    global _ai_client
    try:
        settings = get_settings()
        _ai_client = BaishanAIClient(settings)
        logger.info("Application started, AI client initialized")
    except RuntimeError as exc:
        logger.warning(f"AI client not initialized: {exc}")
        _ai_client = None

    yield  # Application runs here

    # Cleanup on shutdown
    if _ai_client is not None:
        await _ai_client.aclose()
        logger.info("Application shutdown, AI client closed")


app = FastAPI(title="AI 你画我猜", lifespan=lifespan)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    """Serve the frontend drawing page."""
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/guess", response_model=GuessResponse)
async def guess(payload: GuessRequest) -> GuessResponse:
    """Submit drawing strokes and get AI guess."""
    if _ai_client is None:
        detail = "AI client not initialized. Check BAISHAN_API_KEY."
        raise HTTPException(status_code=500, detail=detail)

    prompt = build_guess_prompt(payload)
    logger.info(f"Processing guess request: {len(payload.strokes)} strokes, {len(prompt)} chars")

    try:
        text = await _ai_client.guess(prompt)
    except Exception as exc:
        logger.error(f"AI guess failed: {exc}")
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return GuessResponse(guess=text or "(未识别)", raw_text=text)
