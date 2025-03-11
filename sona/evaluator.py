from chess import (
    BISHOP,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    WHITE,
    Board,
)

from sona import INF

PIECE_MATERIAL = {
    KING: 0,
    PAWN: 1,
    KNIGHT: 3,
    BISHOP: 3,
    ROOK: 5,
    QUEEN: 9,
}


def evaluate(board: Board) -> float:
    if board.is_checkmate():
        return -INF * (1 if board.turn == WHITE else -1)

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_fivefold_repetition()
        or board.can_claim_fifty_moves()
        or board.is_seventyfive_moves()
    ):
        return 0

    material_score = 0
    piece_map = board.piece_map()

    for piece in piece_map.values():
        piece_type = piece.piece_type
        piece_color = piece.color
        piece_value = PIECE_MATERIAL[piece_type]

        material_score += piece_value if piece_color == WHITE else -piece_value

    check_penalty = -3 if board.is_check() else 0

    return material_score + (check_penalty * (1 if board.turn == WHITE else -1))
