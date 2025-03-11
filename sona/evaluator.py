from chess import (
    BISHOP,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    WHITE,
    Board,
    Termination,
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
    sign = 1 if board.turn == WHITE else -1

    outcome = board.outcome()
    if outcome:
        if outcome.termination != Termination.CHECKMATE:
            # Draw
            return 0

        if outcome.winner == WHITE:
            return INF * sign

    material_score = 0
    piece_map = board.piece_map()
    num_pieces_diff = 0

    for piece in piece_map.values():
        color = piece.color
        value = PIECE_MATERIAL[piece.piece_type]

        material_score += value if color == WHITE else -value
        num_pieces_diff += 1 if color == WHITE else -1

    return (material_score + num_pieces_diff) * sign
