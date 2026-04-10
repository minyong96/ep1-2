from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Final

from app.domain.game_state import GameState
from app.storage.abstract_repository import AbstractStateRepository

logger = logging.getLogger(__name__)


class JsonStateRepository(AbstractStateRepository):
    _ENCODING: Final[str] = "utf-8"
    _JSON_INDENT: Final[int] = 4

    def __init__(self, file_path: str | Path) -> None:
        self._file_path: Final[Path] = Path(file_path)

    def load(self) -> GameState:
        if not self._file_path.exists():
            logger.warning("상태 파일이 없어 초기 상태를 생성합니다.")
            return GameState.create_default()

        try:
            with self._file_path.open(encoding=self._ENCODING) as f:
                data = json.load(f)

            logger.info("게임 상태를 불러왔습니다.")
            return GameState.from_dict(data)

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error("파일이 손상되었습니다: %s", e)
            raise RuntimeError(f"상태 파일을 읽을 수 없습니다: {e}") from e

    def save(self, state: GameState) -> None:
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

            with self._file_path.open("w", encoding=self._ENCODING) as f:
                json.dump(state.to_dict(), f, indent=self._JSON_INDENT, ensure_ascii=False)

            logger.info("게임 상태가 저장되었습니다.")

        except IOError as e:
            logger.error("상태 저장 중 오류 발생: %s", e)
            raise OSError(f"상태를 저장할 수 없습니다: {e}") from e