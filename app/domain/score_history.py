from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ScoreHistory:
    played_at: datetime
    quiz_count: int
    score: float

    def __post_init__(self) -> None:
        if self.quiz_count <= 0:
            raise ValueError("퀴즈 수는 1 이상이어야 합니다")
        if not (0.0 <= self.score <= 100.0):
            raise ValueError("점수는 0~100 사이여야 합니다")

    @property
    def formatted_date(self) -> str:
        return self.played_at.strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> dict[str, Any]:
        return {
            "played_at": self.played_at.isoformat(),
            "quiz_count": self.quiz_count,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScoreHistory:
        return cls(
            played_at=datetime.fromisoformat(data["played_at"]),
            quiz_count=data["quiz_count"],
            score=data["score"],
        )