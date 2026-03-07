from app.prompt_builder import build_guess_prompt
from app.schemas import GuessRequest, Stroke, StrokePoint


def test_build_guess_prompt_contains_counts() -> None:
    payload = GuessRequest(
        strokes=[
            Stroke(points=[StrokePoint(x=1, y=2, t=100), StrokePoint(x=3, y=4, t=200)]),
            Stroke(points=[StrokePoint(x=5, y=6, t=300)]),
        ],
        width=640,
        height=400,
    )
    prompt = build_guess_prompt(payload)
    assert "总笔画数: 2" in prompt
    assert "总点数: 3" in prompt
    assert "画布尺寸: 640x400" in prompt
