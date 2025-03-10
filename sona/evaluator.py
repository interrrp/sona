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

from sona import INF


def evaluate(board: Board) -> float:
    if board.is_checkmate():
        return -INF * sign(board.turn)

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
        score -= 3

    n_white_pieces = 0
    n_black_pieces = 0
    for square in SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        score += evaluate_piece(piece)
        if piece.color == WHITE:
            n_white_pieces += 1
        else:
            n_black_pieces += 1

    return score * (n_white_pieces - n_black_pieces) * sign(board.turn)


def evaluate_piece(piece: Piece) -> float:
    return get_piece_material(piece.piece_type)


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


def sign(color: Color) -> float:
    return 1 if color == WHITE else -1
