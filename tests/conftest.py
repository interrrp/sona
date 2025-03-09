import pytest
from chess import Board

from sona.engine import Engine


@pytest.fixture
def board() -> Board:
    return Board()


@pytest.fixture
def engine(board: Board) -> Engine:
    return Engine(board)
