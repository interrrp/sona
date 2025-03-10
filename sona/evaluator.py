from chess import (
    BISHOP,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    SQUARES,
    WHITE,
    Board,
    Color,
    Piece,
    PieceType,
)


def evaluate(board: Board) -> float:
    if board.is_checkmate():
        return worst_score_for(board.turn)

    is_draw = (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_fivefold_repetition()
        or board.can_claim_fifty_moves()
        or board.is_seventyfive_moves()
    )
    if is_draw:
        return 0

    score: float = 0

    if board.is_check():
        score += worst_score_for(board.turn) * 3

    for square in SQUARES:
        piece = board.piece_at(square)
        if piece:
            score += evaluate_piece(piece)

    return score


def evaluate_piece(piece: Piece) -> float:
    sign = 1 if piece.color == WHITE else -1
    return get_piece_material(piece.piece_type) * sign


def get_piece_material(piece_type: PieceType) -> float:
    if piece_type == KING:
        return 0
    if piece_type == PAWN:
        return 1
    if piece_type in (KNIGHT, BISHOP):
        return 3
    if piece_type == ROOK:
        return 5
    if piece_type == QUEEN:
        return 9
    return 0


def worst_score_for(color: Color) -> float:
    return -1 if color == WHITE else 1
