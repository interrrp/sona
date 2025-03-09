import random

from chess import Board, Move


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board
        self.options: dict[str, str | int | bool] = {}

    def move(self) -> Move:
        best_move = self._generate_best_move()
        self._board.push(best_move)
        return best_move

    def _generate_best_move(self) -> Move:
        is_first_move = not self._board.move_stack
        if is_first_move:
            return Move.from_uci("e2e4")

        return random.choice(list(self._board.legal_moves))  # noqa: S311
