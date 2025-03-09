from chess import (
    BISHOP,
    BLACK,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    SQUARES,
    WHITE,
    Board,
    Piece,
    PieceType,
)


def evaluate(board: Board) -> float:
    if board.is_checkmate():
        return -1 if board.turn == WHITE else 1

    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0

    evaluation: float = 0

    if board.is_check():
        if board.turn == WHITE:
            evaluation -= 3
        elif board.turn == BLACK:
            evaluation += 3

    for square in SQUARES:
        piece = board.piece_at(square)
        if piece:
            evaluation += evaluate_piece(piece)

    return evaluation


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
