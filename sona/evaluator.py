from chess import WHITE, Board, square_mirror

from sona.data import PIECE_MATERIAL, PSQTS


def evaluate(board: Board) -> float:
    material_score = 0
    psqt_score = 0

    for square, piece in board.piece_map().items():
        material = PIECE_MATERIAL[piece.piece_type]
        psqt = PSQTS[piece.piece_type]

        if piece.color == WHITE:
            material_score += material
            psqt_score += psqt[square_mirror(square)]
        else:
            material_score -= material
            psqt_score -= psqt[square]

    perspective = 1 if board.turn == WHITE else -1

    return (material_score + psqt_score) * perspective
