EXP = 2         # Hệ số mũ dùng để đánh giá window
INF = 1 << 30
WIN_PTS = INF - 1


class Cell:
    EMPTY: int = 0
    X: int = 1
    O: int = 2


def toCell(s: str):
    match s:
        case "x" | "X":
            return Cell.X
        case "o" | 'O':
            return Cell.O
        case _:
            return Cell.EMPTY


def getOp(role: int):
    return 3 - role
