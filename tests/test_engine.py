from chess import Board

from sona.engine import Engine


def test_engine_makes_move(board: Board, engine: Engine) -> None:
    board.push_uci("e2e4")
    engine.move()
    assert len(board.move_stack) == 2


def test_engine_first_move_is_e4(board: Board, engine: Engine) -> None:
    engine.move()
    assert len(board.move_stack) == 1
    assert board.move_stack[0].uci() == "e2e4"
