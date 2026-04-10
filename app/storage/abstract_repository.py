from abc import ABC, abstractmethod

from app.domain.game_state import GameState

class AbstractStateRepository(ABC):

    @abstractmethod
    def load(self) -> GameState:
        ...

    @abstractmethod
    def save(self, state: GameState) -> None:
        ...