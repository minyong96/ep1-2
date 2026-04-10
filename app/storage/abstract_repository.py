from abc import ABC, abstractmethod

from app.domain.game_state import GameState


class AbstractStateRepository(ABC):

    @abstractmethod
    def load(self) -> GameState:
        """저장된 상태를 불러옵니다. 없으면 기본 상태를 반환합니다."""
        ...

    @abstractmethod
    def save(self, state: GameState) -> None:
        """현재 상태를 저장합니다."""
        ...