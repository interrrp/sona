from dataclasses import dataclass
from typing import Literal

from chess import Board, Move
from chess.polyglot import zobrist_hash

from sona import INF
from sona.evaluator import evaluate


@dataclass(frozen=True)
class TranspositionTableEntry:
    score: float
    depth: int
    flag: Literal["exact", "lowerbound", "upperbound"]


class Engine:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._transposition_table: dict[int, TranspositionTableEntry] = {}
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

    def _negamax(self, depth: int, alpha: float = -INF, beta: float = INF) -> float:  # noqa: C901
        if depth == 0 or self._board.is_game_over():
            return evaluate(self._board)

        board_hash = zobrist_hash(self._board)
        if board_hash in self._transposition_table:
            entry = self._transposition_table[board_hash]
            if entry.depth >= depth:
                if entry.flag == "exact" or alpha >= beta:
                    return entry.score
                if entry.flag == "lowerbound":
                    alpha = max(alpha, entry.score)
                elif entry.flag == "upperbound":
                    beta = min(beta, entry.score)

        original_alpha = alpha
        best_score = -INF
        for move in self._board.legal_moves:
            self._board.push(move)
            score = -self._negamax(depth - 1, -beta, -alpha)
            self._board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        if best_score <= original_alpha:
            flag = "upperbound"
        elif best_score >= beta:
            flag = "lowerbound"
        else:
            flag = "exact"
        self._transposition_table[board_hash] = TranspositionTableEntry(best_score, depth, flag)

        return best_score

    @property
    def _depth(self) -> int:
        specified_depth = self.options.get("Depth")
        if not isinstance(specified_depth, int):
            return 3
        return specified_depth
