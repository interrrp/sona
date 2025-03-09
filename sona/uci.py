from chess import Board

from sona.engine import Engine


def do_uci_command(board: Board, engine: Engine, command: str) -> str:  # noqa: C901, PLR0912, PLR0911
    match command.split():
        case ["uci"]:
            response = "id name Sona\nid author interrrp\n"
            for name, value in engine.options.items():
                response += f"option name {name} type "
                formatted_value = ""
                if isinstance(value, str):
                    response += "string"
                    formatted_value = value
                elif isinstance(value, bool):
                    response += "check"
                    formatted_value = str(value).lower()
                else:
                    response += "spin"
                    formatted_value = value
                response += f" default {formatted_value}\n"
            response += "uciok\n"
            return response

        case ["isready"]:
            return "readyok\n"

        case ["go", "infinite"]:
            move = engine.move()
            return f"bestmove {move.uci()}\n"

        case ["setoption", "name", name, "value", value]:
            if value.isdigit():
                engine.options[name] = int(value)
            elif value in ("true", "false"):
                engine.options[name] = ("false", "true").index(value)
            else:
                engine.options[name] = value
            return ""

        case ["position", "startpos"] | ["ucinewgame"]:
            board.reset()
            return ""

        case ["position", "startpos", "moves", *moves]:
            board.reset()
            for move in moves:
                board.push_uci(move)
            return ""

        case [
            "position",
            "fen",
            fen_part_1,
            fen_part_2,
            fen_part_3,
            fen_part_4,
            fen_part_5,
            fen_part_6,
            "moves",
            *moves,
        ]:
            fen = f"{fen_part_1} {fen_part_2} {fen_part_3} {fen_part_4} {fen_part_5} {fen_part_6}"
            board.set_fen(fen)
            for move in moves:
                board.push_uci(move)
            return ""

        case ["position", "fen", *fen]:
            board.set_fen(" ".join(fen))
            return ""

        case _:
            return "unknown command"
