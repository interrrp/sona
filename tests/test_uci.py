from chess import Board

from sona.engine import Engine
from sona.uci import do_uci_command


def test_uci_uci(board: Board, engine: Engine) -> None:
    engine.options["Life"] = 42
    engine.options["BeastMode"] = True
    engine.options["Type"] = "Fish"

    assert do_uci_command(board, engine, "uci") == (
        "id name Sona\n"
        "id author interrrp\n"
        "option name Life type spin default 42\n"
        "option name BeastMode type check default true\n"
        "option name Type type string default Fish\n"
        "uciok\n"
    )


def test_uci_isready(board: Board, engine: Engine) -> None:
    assert do_uci_command(board, engine, "isready") == "readyok\n"


def test_uci_ucinewgame(board: Board, engine: Engine) -> None:
    assert do_uci_command(board, engine, "ucinewgame") == ""
    assert board.fen() == board.starting_fen
    assert not board.move_stack


def test_uci_goinfinite(board: Board, engine: Engine) -> None:
    assert do_uci_command(board, engine, "go infinite") == "bestmove e2e4\n"
    assert len(board.move_stack) == 1
    assert board.move_stack[0].uci() == "e2e4"


def test_uci_setoption(board: Board, engine: Engine) -> None:
    engine.options["Life"] = 42
    engine.options["BeastMode"] = True
    engine.options["Type"] = "Salmon"

    responses: list[str] = []
    responses.append(do_uci_command(board, engine, "setoption name Life value 43"))
    responses.append(do_uci_command(board, engine, "setoption name BeastMode value false"))
    responses.append(do_uci_command(board, engine, "setoption name Type value Salmon"))
    assert responses == ["", "", ""]

    assert engine.options["Life"] == 43
    assert not engine.options["BeastMode"]
    assert engine.options["Type"] == "Salmon"


def test_uci_position_startpos(board: Board, engine: Engine) -> None:
    assert do_uci_command(board, engine, "position startpos") == ""
    assert board.fen() == board.starting_fen
    assert not board.move_stack


def test_uci_position_fen(board: Board, engine: Engine) -> None:
    e4_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    assert do_uci_command(board, engine, f"position fen {e4_fen}") == ""
    assert board.fen() == e4_fen


def test_uci_position_fen_and_moves(board: Board, engine: Engine) -> None:
    e4_e5_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    e4_e5_g1f3_d7d6_fen = "rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 2"
    assert do_uci_command(board, engine, f"position fen {e4_e5_fen} moves g1f3 d7d6") == ""
    assert board.fen() == e4_e5_g1f3_d7d6_fen


def test_uci_position_startpos_and_moves(board: Board, engine: Engine) -> None:
    assert do_uci_command(board, engine, "position startpos moves e2e4 e7e5") == ""
    assert len(board.move_stack) == 2
    assert board.move_stack[0].uci() == "e2e4"
    assert board.move_stack[1].uci() == "e7e5"
