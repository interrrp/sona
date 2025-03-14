from chess import BISHOP, KING, KNIGHT, PAWN, QUEEN, ROOK, WHITE, Board, Termination

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
    outcome = board.outcome()
    if outcome:
        if outcome.termination != Termination.CHECKMATE:
            # Draw
            return 0
        # Checkmate
        return -INF

    material_score = 0
    num_pieces_diff = 0

    for piece in board.piece_map().values():
        if piece.color == WHITE:
            material_score += PIECE_MATERIAL[piece.piece_type]
            num_pieces_diff += 1
        else:
            material_score -= PIECE_MATERIAL[piece.piece_type]
            num_pieces_diff -= 1

    sign = 1 if board.turn == WHITE else -1

    return (material_score + num_pieces_diff) * sign
