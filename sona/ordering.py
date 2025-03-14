from collections.abc import Generator

from chess import Board, Move

from sona.evaluator import PIECE_MATERIAL


def ordered_moves(board: Board) -> Generator[Move]:
    def move_ordering_key(move: Move) -> float:
        guess = 0

        move_piece_type = board.piece_type_at(move.from_square)
        if not move_piece_type:
            return 0

        target_piece_type = board.piece_type_at(move.to_square)
        if target_piece_type:
            guess += PIECE_MATERIAL[target_piece_type] - PIECE_MATERIAL[move_piece_type]

        if move.promotion:
            guess += PIECE_MATERIAL[move.promotion]

        return guess

    all_moves = list(board.legal_moves)
    while all_moves:
        best_move = min(all_moves, key=move_ordering_key)
        all_moves.remove(best_move)
        yield best_move
