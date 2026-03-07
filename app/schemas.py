from __future__ import annotations

from pydantic import BaseModel, Field


class StrokePoint(BaseModel):
    x: float = Field(..., ge=0.0)
    y: float = Field(..., ge=0.0)
    t: int = Field(..., ge=0)


class Stroke(BaseModel):
    points: list[StrokePoint]


class GuessRequest(BaseModel):
    strokes: list[Stroke]
    width: int = Field(..., ge=1, le=5000)
    height: int = Field(..., ge=1, le=5000)


class GuessResponse(BaseModel):
    guess: str
    raw_text: str
