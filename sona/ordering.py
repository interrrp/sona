from chess import Board, Move

from sona.data import PIECE_MATERIAL


def ordered_moves(board: Board) -> list[Move]:
    def move_ordering_key(move: Move) -> float:
        guess = 0

        move_piece_type = board.piece_type_at(move.from_square)
        if not move_piece_type:
            return 1000

        target_piece_type = board.piece_type_at(move.to_square)
        if target_piece_type:
            guess += 10 * (PIECE_MATERIAL[target_piece_type] - PIECE_MATERIAL[move_piece_type])

        if move.promotion:
            guess += 100 * PIECE_MATERIAL[move.promotion]

        return guess

    return sorted(board.legal_moves, key=move_ordering_key)
