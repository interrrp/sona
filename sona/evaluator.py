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
    PieceType,
)

from sona import INF


def evaluate(board: Board) -> float:
    if board.is_checkmate():
        return -INF * get_sign(board)

    if is_draw(board):
        return 0

    return get_material_weight(board) * get_piece_diff(board) * get_sign(board)


def is_draw(board: Board) -> bool:
    return (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_fivefold_repetition()
        or board.can_claim_fifty_moves()
        or board.is_seventyfive_moves()
    )


def get_material_weight(board: Board) -> float:
    weight = 0
    for square in SQUARES:
        piece = board.piece_at(square)
        if piece:
            weight += get_piece_material(piece.piece_type)
    return weight


def get_piece_diff(board: Board) -> float:
    num_white_pieces = 0
    num_black_pieces = 0

    for square in SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        if piece.color == WHITE:
            num_white_pieces += 1
        else:
            num_black_pieces += 1

    return num_white_pieces - num_black_pieces


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


def get_sign(board: Board) -> float:
    return 1 if board.turn == WHITE else -1
