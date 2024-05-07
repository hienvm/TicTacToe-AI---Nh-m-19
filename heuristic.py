from collections import deque
from typing import Iterable, Literal

from util import EXP, WIN_PTS

def evaluate(board: list[list[str]], k: int, role: Literal['x', 'o'], op_role: Literal['x', 'o']) -> int:
    '''Thuật toán tính heuristic: sliding window kích thước k cho từng hàng, cột và đường chéo'''
    total = 0
    m = len(board)
    n = len(board[0])

    # Tính điểm các hàng
    if n >= k:
        for i in range(m):
            tmp = evaluate_ln(k, role, op_role,
                              [board[i][j] for j in range(n)])
            if abs(tmp) == WIN_PTS:
                # print(board)
                return tmp
            total += tmp

    # Tính điểm các cột
    if m >= k:
        for j in range(n):
            tmp = evaluate_ln(k, role, op_role,
                              [board[i][j] for i in range(m)])
            if abs(tmp) == WIN_PTS:
                # print(board)
                return tmp
            total += tmp

    # Tính điểm các đường chéo xuống từ trái sang i - j = c
    for c in range(- n + 1, m - 1):
        # Ta có: 0 <= i < m && i = j + c && 0 <= j < n
        # Suy ra: 0 <= j + c < m && 0 <= j < n
        low = max(0, -c)
        upper = min(m - c, n)
        if upper - low >= k:
            tmp = evaluate_ln(k, role, op_role,
                              [board[j + c][j] for j in range(low, upper)])
            if abs(tmp) == WIN_PTS:
                # print(board)
                return tmp
            total += tmp

    # Tính điểm các đường chéo lên từ trái sang i + j = c
    for c in range(0, m + n - 1):
        # Ta có: 0 <= i < m && i = c - j && 0 <= j < n
        # Suy ra: 0 <= c - j < m && 0 <= j < n
        # Suy ra: c - m < j && j <= c && 0 <= j < n
        low = max(0, c - m + 1)
        upper = min(c + 1, n)
        if upper - low >= k:
            tmp = evaluate_ln(k, role, op_role,
                              [board[c - j][j] for j in range(low, upper)])
            if abs(tmp) == WIN_PTS:
                # print(board)
                return tmp
            total += tmp

    return total


def evaluate_ln(k: int, role: Literal['x', 'o'], op_role: Literal['x', 'o'], ln: Iterable[str]):
    total = 0
    window = deque(maxlen=k)    # window: một dãy k ô liên tiếp
    # đếm sl các ô của mỗi bên trong window
    self_cnt: int = 0
    op_cnt: int = 0

    # Duyệt từng ô
    for cell in ln:
        # Thêm ô tiếp theo vào cuối window
        window.append(cell)
        if cell == role:
            self_cnt += 1
        elif cell == op_role:
            op_cnt += 1

        if len(window) == k:
            # Đánh giá window
            if self_cnt > 0:
                if op_cnt == 0:         # Khi window chứa ô của bên mình và không chứa ô của đối thủ
                    if self_cnt == k:   # Thắng
                        return WIN_PTS
                    else:
                        # Công thức tính điểm của window cho bên mình: 2^(EXP * số ô bên mình)
                        total += 1 << (EXP * (self_cnt - 1))
            elif op_cnt > 0:            # Khi window chứa ô của đối thủ và không chứa ô của bên mình
                if op_cnt == k:         # Thua
                    return -WIN_PTS
                else:
                    # Công thức tính điểm của window cho đối thủ: 2^(EXP * số ô đối thủ)
                    total -= 1 << (EXP * (op_cnt - 1))

            # loại bỏ phần tử đầu khi window đã đạt đủ kích thước k
            first = window.popleft()
            if first == role:
                self_cnt -= 1
            elif first == op_role:
                op_cnt -= 1

    return total
