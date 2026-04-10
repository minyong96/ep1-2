from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_CHOICE_COUNT = 4
_VALID_ANSWERS = frozenset(range(1, _CHOICE_COUNT + 1))


@dataclass(frozen=True)
class Quiz:
    question: str
    choices: tuple[str, ...]
    answer: int
    hint: str | None = None

    def __post_init__(self) -> None:
        self._validate()

    # ── 검증 ──────────────────────────────────────────

    def _validate(self) -> None:
        self._validate_question()
        self._validate_choices()
        self._validate_answer()
        self._validate_hint()

    def _validate_question(self) -> None:
        if not self.question.strip():
            raise ValueError("질문이 비어 있습니다")

    def _validate_choices(self) -> None:
        if len(self.choices) != _CHOICE_COUNT:
            raise ValueError(f"선택지는 {_CHOICE_COUNT}개여야 합니다")

        empty = [i + 1 for i, c in enumerate(self.choices) if not c.strip()]
        if empty:
            raise ValueError(f"선택지 {empty}번이 비어 있습니다")

    def _validate_answer(self) -> None:
        if self.answer not in _VALID_ANSWERS:
            raise ValueError(
                f"정답은 1~{_CHOICE_COUNT} 사이여야 합니다. 입력값: {self.answer}"
            )

    def _validate_hint(self) -> None:
        if self.hint is not None and not self.hint.strip():
            raise ValueError("힌트는 비어 있을 수 없습니다")

    # ── 동작 ──────────────────────────────────────────

    def display(self, show_hint: bool = False) -> None:
        print(f"\n[문제] {self.question}")

        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

        if show_hint and self.hint:
            print(f"\n💡 힌트: {self.hint}")

    def is_correct(self, submitted: int) -> bool:
        return self.answer == submitted

    def get_hint(self) -> str | None:
        return self.hint

    # ── 직렬화 ────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Quiz:
        return cls(
            question=data["question"],
            choices=tuple(data["choices"]),
            answer=data["answer"],
            hint=data.get("hint"),  # 없으면 None
        )