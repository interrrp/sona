import random

from chess import BLACK, WHITE, Board, Color, Move

from sona.evaluator import evaluate


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

        color = self._board.turn
        opposite_color = not color

        legal_moves = list(self._board.legal_moves)

        best_move = random.choice(legal_moves)  # noqa: S311
        best_score: float = -1 if color == WHITE else 1

        for move in legal_moves:
            self._board.push(move)
            score = self._minimax(3, opposite_color)
            self._board.pop()

            if (color == WHITE and score > best_score) or (color == BLACK and score < best_score):
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, depth: int, color: Color, alpha: float = -1000, beta: float = 1000) -> float:
        if depth == 0 or self._board.is_game_over():
            return evaluate(self._board)

        best_score: float = -1 if color == WHITE else 1

        for move in self._board.legal_moves:
            self._board.push(move)
            score = self._minimax(depth - 1, not color, alpha, beta)
            self._board.pop()

            if (color == WHITE and score > best_score) or (color == BLACK and score < best_score):
                best_score = score

            if color == WHITE:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

            if beta <= alpha:
                break

        return best_score
