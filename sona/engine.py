from chess import Board, Move
from chess.polyglot import zobrist_hash

from sona import INF
from sona.evaluator import evaluate


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._score_cache: dict[int, float] = {}
        self.options: dict[str, str | int | bool] = {"Depth": 3}

    def move(self) -> Move:
        best_move = self._generate_best_move()
        self._board.push(best_move)
        return best_move

    def _generate_best_move(self) -> Move:
        if not self._board.move_stack:
            # First move should always be e2e4
            return Move.from_uci("e2e4")

        all_moves = list(self._board.legal_moves)
        best_move = all_moves[0]
        best_score = -INF

        for move in all_moves:
            self._board.push(move)
            score = -self._negamax(depth=self._depth)
            self._board.pop()

            if score >= best_score:
                best_score = score
                best_move = move

        return best_move

    def _negamax(self, depth: int, alpha: float = -INF, beta: float = INF) -> float:
        if depth == 0 or self._board.is_game_over():
            return evaluate(self._board)

        board_hash = zobrist_hash(self._board)
        if score := self._score_cache.get(board_hash):
            return score

        score = -INF
        for move in self._board.legal_moves:
            self._board.push(move)
            score = max(score, -self._negamax(depth - 1, -beta, -alpha))
            self._board.pop()

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        self._score_cache[board_hash] = score

        return score

    @property
    def _depth(self) -> int:
        specified_depth = self.options.get("Depth")
        if not isinstance(specified_depth, int):
            return 3
        return specified_depth
