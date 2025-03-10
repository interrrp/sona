import pytest
from chess import Board

from sona import INF
from sona.evaluator import evaluate

WHITE_WINNING_FEN = "rnbq1bnr/ppppkppp/8/4Q3/4P3/8/PPPP1PPP/RNB1KBNR b KQ - 0 3"
BLACK_WINNING_FEN = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
STALEMATE_FEN = "8/8/8/8/8/8/7k/7K b - - 0 1"
INSUFFICIENT_MATERIAL_FEN = "8/8/8/8/8/8/7k/K7 w - - 0 1"
SEVENTYFIVE_MOVE_FEN = "8/8/8/8/8/8/8/8 w - - 75 1"


@pytest.mark.parametrize(
    ("fen", "expected_evaluation"),
    [
        (WHITE_WINNING_FEN, INF),
        (BLACK_WINNING_FEN, -INF),
        (STALEMATE_FEN, 0),
        (INSUFFICIENT_MATERIAL_FEN, 0),
        (SEVENTYFIVE_MOVE_FEN, 0),
    ],
)
def test_evaluator(board: Board, fen: str, expected_evaluation: str) -> None:
    board.set_fen(fen)
    assert evaluate(board) == expected_evaluation
