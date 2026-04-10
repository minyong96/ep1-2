from __future__ import annotations

import random

from app.domain.game_state import GameState
from app.domain.quiz import Quiz
from app.storage.abstract_repository import AbstractStateRepository  # 구체 클래스 아닌 추상에 의존


class QuizService:

    def __init__(self, repository: AbstractStateRepository) -> None:
        self._repository = repository
        self._state: GameState = self._load_state()

    # ── 조회 ──────────────────────────────────────────

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def quizzes(self) -> list[Quiz]:
        return self._state.quizzes

    @property
    def best_score(self) -> float:
        return self._state.best_score

    # ── 퀴즈 관리 ─────────────────────────────────────

    def add_quiz(self, quiz: Quiz) -> None:
        self._state.add_quiz(quiz)

    def remove_quiz_at(self, index: int) -> Quiz:
        if not (1 <= index <= len(self.quizzes)):
            raise ValueError(f"유효하지 않은 퀴즈 번호입니다: {index}")
        quiz = self.quizzes[index - 1]
        self._state.remove_quiz(quiz)
        return quiz

    def sample_quizzes(self, count: int) -> list[Quiz]:
        if count > len(self.quizzes):
            raise ValueError(f"퀴즈 수({len(self.quizzes)})보다 많이 요청했습니다: {count}")
        return random.sample(self.quizzes, count)

    # ── 점수 처리 ─────────────────────────────────────

    def calculate_score(self, correct: int, hint_used: int) -> float:
        return max(0.0, correct - hint_used * 0.5)

    def record_result(self, score: float, quiz_count: int) -> bool:
        return self._state.record_score(score)

    # ── 저장 ──────────────────────────────────────────

    def save(self) -> None:
        self._repository.save(self._state)

    # ── 내부 ──────────────────────────────────────────

    def _load_state(self) -> GameState:
        try:
            return self._repository.load()
        except RuntimeError:
            return GameState.create_default()