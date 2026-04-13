from __future__ import annotations

from typing import Final

from app.domain.quiz import Quiz
from app.service.quiz_service import QuizService


class QuizGame:
    _EXIT_OPTION: Final[int] = 7

    def __init__(self, service: QuizService) -> None:
        self._service = service

    # ── 진입점 ────────────────────────────────────────

    def run(self) -> None:
        print("Quiz Game 시작")
        try:
            while True:
                self._show_menu()
                choice = self._get_int_input("메뉴 선택: ", range(1, self._EXIT_OPTION + 1))
                self._handle_menu(choice)
        except KeyboardInterrupt:
            print()
            print("사용자에 의해 종료되었습니다.")
            self._shutdown()
        finally:
            self._shutdown()

    def _handle_menu(self, choice: int) -> None:
        actions = {
            1: self._play_quiz,
            2: self._add_quiz,
            3: self._list_quizzes,
            4: self._show_best_score,
            5: self._delete_quiz,
            6: self._show_score_histories,
            7: self._exit,
        }
        actions[choice]()

    # ── 메뉴 ──────────────────────────────────────────

    def _show_menu(self) -> None:
        print()
        print("=" * 40)
        print("        Python Quiz Game")
        print("=" * 40)
        print(f"퀴즈 개수: {len(self._service.quizzes)}")
        print(f"최고 점수: {self._service.best_score}")
        print()
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 점수 기록 히스토리")
        print("7. 종료")

    # ── 퀴즈 풀기 ─────────────────────────────────────

    def _play_quiz(self) -> None:
        if not self._service.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        count = self._get_int_input(
            prompt="몇 문제를 풀까요? ",
            valid_range=range(1, len(self._service.quizzes) + 1),
        )

        selected = self._service.sample_quizzes(count)
        correct, hint_used, final_score, is_new_best = 0, 0, 0, False

        for quiz in selected:
            is_correct, used_hint = self._ask_question(quiz)
            print("정답입니다." if is_correct else "오답입니다.")
            if is_correct:
                correct += 1
            if used_hint:
                hint_used += 1
            final_score = self._service.calculate_score(correct, hint_used)
            is_new_best = self._service.record_result(final_score, count)


        print(f"\n총 점수: {final_score}")
        if is_new_best:
            print("최고 점수를 갱신했습니다!")

    def _ask_question(self, quiz: Quiz) -> tuple[bool, bool]:
        quiz.display()

        if quiz.hint:
            print("5. 힌트 보기")

        used_hint = False

        while True:
            valid_range = range(1, 6) if quiz.hint else range(1, 5)
            answer = self._get_int_input("번호 입력: ", valid_range)

            if answer == 5 and quiz.hint:
                print(f"힌트: {quiz.hint}")
                used_hint = True
                continue

            return quiz.is_correct(answer), used_hint

    # ── 퀴즈 관리 ─────────────────────────────────────

    def _add_quiz(self) -> None:
        print("\n새 퀴즈를 추가합니다.")
        question = input("문제: ").strip()
        choices = tuple(input(f"선택지 {i}: ").strip() for i in range(1, 5))
        answer = self._get_int_input("정답 번호: ", range(1, 5))
        hint_input = input("힌트(없으면 엔터): ").strip()

        try:
            self._service.add_quiz(Quiz(
                question=question,
                choices=choices,
                answer=answer,
                hint=hint_input or None,
            ))
            print("퀴즈가 추가되었습니다.")

        except ValueError as e:
            print(f"퀴즈 생성 실패: {e}")

    def _list_quizzes(self) -> None:
        if not self._service.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print()
        for idx, quiz in enumerate(self._service.quizzes, 1):
            hint_text = " / 힌트 있음" if quiz.hint else ""
            print(f"{idx}. {quiz.question}{hint_text}")

    def _delete_quiz(self) -> None:
        if not self._service.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        self._list_quizzes()

        choice = self._get_int_input(
            prompt="삭제할 퀴즈 번호 입력: ",
            valid_range=range(1, len(self._service.quizzes) + 1),
        )

        try:
            deleted = self._service.remove_quiz_at(choice)
            print(f"삭제되었습니다: {deleted.question}")
        except ValueError as e:
            print(f"삭제 실패: {e}")

    # ── 점수 확인 ─────────────────────────────────────

    def _show_best_score(self) -> None:
        print(f"\n현재 최고 점수: {self._service.best_score}")

    def _show_score_histories(self) -> None:
        histories = self._service.state.score_histories

        if not histories:
            print("기록된 점수 히스토리가 없습니다.")
            return

        print("\n점수 기록 히스토리")
        for idx, h in enumerate(histories, 1):
            print(f"{idx}. {h.formatted_date} / {h.quiz_count}문제 / {h.score}점")

    # ── 입력 유틸 ─────────────────────────────────────

    def _get_int_input(self, prompt: str, valid_range: range) -> int:
        while True:
            try:
                raw = input(prompt).strip()

                if not raw:
                    print("입력이 비어 있습니다.")
                    continue

                value = int(raw)

                if value not in valid_range:
                    print(f"{valid_range.start}~{valid_range.stop - 1} 사이 숫자를 입력하세요.")
                    continue

                return value

            except ValueError:
                print("숫자를 입력하세요.")

            except EOFError:
                print()
                self._shutdown()
                raise SystemExit

    # ── 종료 ──────────────────────────────────────────

    def _exit(self) -> None:
        self._shutdown()
        raise SystemExit

    def _shutdown(self) -> None:
        print("상태 저장 중...")
        self._service.save()
        print("프로그램 종료")