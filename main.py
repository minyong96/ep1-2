from pathlib import Path

from app.storage.json_state_repository import JsonStateRepository
from app.service.quiz_service import QuizService
from app.ui.quiz_game import QuizGame

STATE_FILE_PATH = Path("data/state.json")


def main() -> None:

    print("프로그램을 시작합니다.")

    repository = JsonStateRepository(STATE_FILE_PATH)
    service = QuizService(repository)
    game = QuizGame(service)
    game.run()


if __name__ == "__main__":

    main()