from chess import Board, Move

from sona import INF
from sona.evaluator import evaluate
from sona.ordering import ordered_moves


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board
        self.options: dict[str, str | int | bool] = {"Depth": 3}

    def move(self) -> Move:
        best_move = self._generate_best_move()
        self._board.push(best_move)
        return best_move

    def _generate_best_move(self) -> Move:
        board = self._board

        if not board.move_stack:
            # First move should always be e2e4
            return Move.from_uci("e2e4")

        best_move = Move.null()
        best_score = -INF

        for move in board.legal_moves:
            board.push(move)
            score = -self._search(self._depth)
            board.pop()

            if score >= best_score:
                best_score = score
                best_move = move

        return best_move

    def _search(self, depth: int, _alpha: float = -INF, _beta: float = INF) -> float:
        board = self._board

        if depth == 0 or board.is_game_over():
            return evaluate(board)

        for move in ordered_moves(board):
            board.push(move)
            score = -self._search(depth - 1, -_beta, -_alpha)
            board.pop()

            if score >= _beta:
                return _beta

            _alpha = max(_alpha, score)

        return _alpha

    @property
    def _depth(self) -> int:
        specified_depth = self.options.get("Depth")
        if not isinstance(specified_depth, int):
            return 3
        return specified_depth
