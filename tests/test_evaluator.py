import pytest
from chess import Board

from sona import INF
from sona.evaluator import evaluate

WHITE_WINNING_FEN = "pkp5/8/1Q6/1K6/8/8/8/8 b - - 0 1"
BLACK_WINNING_FEN = "PKP5/8/1q6/1k6/8/8/8/8 w - - 0 1"
STALEMATE_FEN = "8/8/8/8/8/8/7k/7K b - - 0 1"
INSUFFICIENT_MATERIAL_FEN = "8/8/8/8/8/8/7k/K7 w - - 0 1"
SEVENTYFIVE_MOVE_FEN = "8/8/8/8/8/8/8/8 w - - 75 1"


@pytest.mark.parametrize(
    ("fen", "expected_evaluation"),
    [
        (WHITE_WINNING_FEN, -INF),
        (BLACK_WINNING_FEN, -INF),
        (STALEMATE_FEN, 0),
        (INSUFFICIENT_MATERIAL_FEN, 0),
        (SEVENTYFIVE_MOVE_FEN, 0),
    ],
    ids=[
        "white wins from black's perspective",
        "black wins from white's perspective",
        "stalemate",
        "insufficient material",
        "seventy-five moves",
    ],
)
def test_evaluator(board: Board, fen: str, expected_evaluation: str) -> None:
    board.set_fen(fen)
    assert evaluate(board) == expected_evaluation
