from chess import Board

from sona.engine import Engine
from sona.uci import do_uci_command


def main() -> None:
    board = Board()
    engine = Engine(board)

    while True:
        command = input()
        response = do_uci_command(board, engine, command)
        print(response, end="")  # noqa: T201


if __name__ == "__main__":
    main()
