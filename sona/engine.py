import random

from chess import Board


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board

    def move(self) -> None:
        is_first_move = len(self._board.move_stack) == 0
        if is_first_move:
            self._board.push_uci("e2e4")
            return

        self._board.push(random.choice(list(self._board.legal_moves)))  # noqa: S311
