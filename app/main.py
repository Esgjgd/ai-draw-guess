from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.ai_client import BaishanAIClient
from app.config import get_settings
from app.prompt_builder import build_guess_prompt
from app.schemas import GuessRequest, GuessResponse

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = FastAPI(title="AI 你画我猜")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/guess", response_model=GuessResponse)
async def guess(payload: GuessRequest) -> GuessResponse:
    try:
        settings = get_settings()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    prompt = build_guess_prompt(payload)
    logger.info(f"Built prompt: {prompt[:200]}...")  # Log first 200 chars
    
    client = BaishanAIClient(settings)
    try:
        text = await client.guess(prompt)
        logger.info(f"AI guess result: {text}")
    except Exception as exc:  # pragma: no cover - external error
        logger.error(f"AI guess failed: {exc}")
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return GuessResponse(guess=text or "(未识别)", raw_text=text)
