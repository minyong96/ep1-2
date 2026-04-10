from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.quiz import Quiz
from app.domain.score_history import ScoreHistory


@dataclass
class GameState:
    quizzes: list[Quiz]
    best_score: float = 0.0
    score_histories: list[ScoreHistory] = field(default_factory=list)

    # ── 조회 ──────────────────────────────────────────

    @property
    def quiz_count(self) -> int:
        return len(self.quizzes)

    @property
    def has_history(self) -> bool:
        return len(self.score_histories) > 0

    @property
    def latest_history(self) -> ScoreHistory | None:
        return self.score_histories[-1] if self.has_history else None

    # ── 동작 ──────────────────────────────────────────

    def record_score(self, score: float) -> None:
        history = ScoreHistory(
            played_at=datetime.now(),
            quiz_count=self.quiz_count,
            score=score,
        )
        self.score_histories.append(history)

        self.best_score = max(self.best_score, score)

    def add_quiz(self, quiz: Quiz) -> None:
        self.quizzes.append(quiz)

    def remove_quiz(self, quiz: Quiz) -> None:
        self.quizzes.remove(quiz)

    # ── 직렬화 ────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        return {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "score_histories": [h.to_dict() for h in self.score_histories],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        return cls(
            quizzes=[Quiz.from_dict(q) for q in data.get("quizzes", [])],
            best_score=data.get("best_score", 0.0),
            score_histories=[
                ScoreHistory.from_dict(h)
                for h in data.get("score_histories", [])
            ],
        )

    @classmethod
    def create_default(cls) -> GameState:
        return cls(quizzes=_default_quizzes())


# ── 기본 퀴즈 데이터 ──────────────────

def _default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            question="Python의 창시자는 누구인가?",
            choices=("Guido van Rossum", "Linus Torvalds", "James Gosling", "Bjarne Stroustrup"),
            answer=1,
            hint= "파이썬 언어를 만든 네덜란드 출신 개발자이다."
        ),
        Quiz(
            question="문자열 길이를 구하는 함수는?",
            choices=("size()", "length()", "count()", "len()"),
            answer=4,
            hint= "파이썬 내장 함수이다"
        ),
        Quiz(
            question="조건문을 시작할 때 사용하는 키워드는?",
            choices=("for", "while", "if", "switch"),
            answer=3,
            hint= "C, Java와 비슷한 키워드다."
        ),
        Quiz(
            question="반복문에 올바른 키워드는?",
            choices=("repeat", "loop", "for", "iterate"),
            answer=3,
            hint= "for-in 구문으로 자주 쓴다."
        ),
    ]