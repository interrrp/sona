from chess import Board, Move, Termination

from sona.data import INF
from sona.evaluator import evaluate
from sona.ordering import ordered_moves


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board
        self.options = Options()

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
            score = -self._search(self.options.depth)
            board.pop()

            if score >= best_score:
                best_score = score
                best_move = move

        return best_move

    def _search(self, depth: int, _alpha: float = -INF, _beta: float = INF) -> float:
        board = self._board

        outcome = board.outcome()
        if outcome:
            if outcome.termination != Termination.CHECKMATE:
                # Draw
                return 0
            # Checkmate
            return -INF

        if depth == 0:
            return evaluate(board)

        for move in ordered_moves(board):
            board.push(move)
            score = -self._search(depth - 1, -_beta, -_alpha)
            board.pop()

            if score >= _beta:
                return _beta

            _alpha = max(_alpha, score)

        return _alpha


class Options(dict[str, str | int | bool]):
    def __init__(self) -> None:
        self["Depth"] = 3

    @property
    def depth(self) -> int:
        return int(self["Depth"])
