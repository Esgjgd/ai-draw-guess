from __future__ import annotations

from app.schemas import GuessRequest


def build_guess_prompt(payload: GuessRequest) -> str:
    stroke_count = len(payload.strokes)
    points_count = sum(len(s.points) for s in payload.strokes)
    summary = (
        "你是一个绘画猜测AI。根据画布上的绘画笔迹，推断出绘制的物体。只返回猜测的物体名称，用中文，不要任何解释或额外内容。"
    )
    meta = (
        f"画布尺寸: {payload.width}x{payload.height}. 总笔画数: {stroke_count}. 总点数: {points_count}.\n"
    )

    serialized = []
    for stroke in payload.strokes:
        points = [f"({p.x:.1f},{p.y:.1f},{p.t})" for p in stroke.points]
        serialized.append(" -> ".join(points))

    content = "\n".join(serialized) if serialized else "(empty)"
    return f"{summary}{meta}笔画:\n{content}"
