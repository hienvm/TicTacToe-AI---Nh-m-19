from collections import deque
import numpy as np
from itertools import repeat

from util import EXP, WIN_PTS, Cell, getOp


class Heuristic:
    def __init__(self, k, role) -> None:
        self.k = k
        self.role = role

        # direction matrices
        # ánh xạ từ chỉ số (i, j) của phần tử đầu tiên -> điểm số của window
        self.horizontal: np.ndarray
        self.vertical: np.ndarray
        self.desclr: np.ndarray
        self.asclr: np.ndarray

    def build(self, board: np.ndarray):
        '''Thuật toán tính heuristic: sliding window kích thước k cho từng hàng, cột và đường chéo'''
        total = 0
        self.board = board
        m = len(board)
        n = len(board[0])
        self.horizontal = np.zeros((m, n), dtype=np.int64)
        self.vertical = np.zeros((m, n), dtype=np.int64)
        self.desclr = np.zeros((m, n), dtype=np.int64)
        self.asclr = np.zeros((m, n), dtype=np.int64)

        # Tính điểm các hàng
        if n >= self.k:
            for i in range(m):
                tmp = self.evaluate_ln(zip(repeat(i), range(n)),
                                       self.horizontal,
                                       )
                if abs(tmp) == WIN_PTS:
                    return tmp
                total += tmp

        # Tính điểm các cột
        if m >= self.k:
            for j in range(n):
                tmp = self.evaluate_ln(zip(range(m), repeat(j)),
                                       self.vertical,
                                       )
                if abs(tmp) == WIN_PTS:
                    return tmp
                total += tmp

        # Tính điểm các đường chéo xuống từ trái sang i - j = c
        for c in range(- n + 1, m - 1):
            # Ta có: 0 <= i < m && i = j + c && 0 <= j < n
            # Suy ra: 0 <= j + c < m && 0 <= j < n
            lowj = max(0, -c)
            highj = min(m - c, n)
            if highj - lowj >= self.k:
                tmp = self.evaluate_ln(zip(range(lowj + c, highj + c),
                                           range(lowj, highj)),
                                       self.desclr,
                                       )
                if abs(tmp) == WIN_PTS:
                    return tmp
                total += tmp

        # Tính điểm các đường chéo lên từ trái sang i + j = c
        for c in range(0, m + n - 1):
            # Ta có: 0 <= i < m && i = c - j && 0 <= j < n
            # Suy ra: 0 <= c - j < m && 0 <= j < n
            # Suy ra: c - m < j && j <= c && 0 <= j < n
            lowj = max(0, c - m + 1)
            highj = min(c + 1, n)
            if highj - lowj >= self.k:
                tmp = self.evaluate_ln(zip(range(c - lowj, c - highj, -1),
                                           range(lowj, highj)),
                                       self.asclr,
                                       )
                if abs(tmp) == WIN_PTS:
                    return tmp
                total += tmp

    def sum(self) -> int:
        return self.horizontal.sum() + self.vertical.sum() + self.desclr.sum() + self.asclr.sum()

    def update(self, i, j):
        m = len(self.board)
        n = len(self.board[0])
        k = self.k
        total = 0
        # Tính điểm hàng
        score = self.evaluate_ln(
            zip(
                repeat(i),
                range(
                    max(0, j - k + 1),
                    min(n, j + k)
                )
            ),
            self.horizontal
        )
        if abs(score) == WIN_PTS:
            return score
        total += score
        # Tính điểm cột
        score = self.evaluate_ln(
            zip(
                range(
                    max(0, i - k + 1),
                    min(m, i + k)
                ),
                repeat(j)
            ),
            self.vertical
        )
        if abs(score) == WIN_PTS:
            return score
        total += score
        # Tính điểm đường chéo xuống từ trái sang i - j = c
        self.evaluate_ln(
            [
                (i, j) for i, j in zip(
                    range(i - k + 1, i + k),
                    range(j - k + 1, j + k)
                )
                if 0 <= i < m and 0 <= j < n
            ],
            self.desclr
        )
        if abs(score) == WIN_PTS:
            return score
        total += score
        # Tính điểm đường chéo lên từ trái sang i + j = c
        self.evaluate_ln(
            [
                (i, j) for i, j in zip(
                    range(i + k - 1, i - k, -1),
                    range(j - k + 1, j + k)
                )
                if 0 <= i < m and 0 <= j < n
            ],
            self.asclr
        )
        if abs(score) == WIN_PTS:
            return score
        total += score
        return total

    def evaluate_ln(self, indices, direction_matrix):
        board = self.board
        total = 0
        # đếm sl các ô của mỗi bên trong window
        self_cnt: int = 0
        op_cnt: int = 0
        role = self.role
        k = self.k
        op_role = getOp(role)

        window = deque(maxlen=self.k)    # window: một dãy k ô liên tiếp

        # Duyệt từng ô
        for i, j in indices:
            cell = board[i][j]
            # Thêm ô tiếp theo vào cuối window
            window.append((cell, i, j))
            if cell == role:
                self_cnt += 1
            elif cell == op_role:
                op_cnt += 1

            if len(window) == k:
                window_score = 0
                # Đánh giá window
                if self_cnt > 0:
                    if op_cnt == 0:         # Khi window chứa ô của bên mình và không chứa ô của đối thủ
                        if self_cnt == k:   # Thắng
                            window_score = WIN_PTS
                        else:
                            # Công thức tính điểm của window cho bên mình: 2^(EXP * số ô bên mình)
                            window_score = 1 << (EXP * (self_cnt - 1))
                elif op_cnt > 0:            # Khi window chứa ô của đối thủ và không chứa ô của bên mình
                    if op_cnt == k:         # Thua
                        window_score = - WIN_PTS
                    else:
                        # Công thức tính điểm của window cho đối thủ: 2^(EXP * số ô đối thủ)
                        window_score = -(1 << (EXP * (op_cnt - 1)))
                # loại bỏ phần tử đầu khi window đã đạt đủ kích thước k
                first, fi, fj = window.popleft()
                direction_matrix[fi][fj] = window_score
                if abs(window_score) == WIN_PTS:
                    return window_score
                total += window_score
                if first == role:
                    self_cnt -= 1
                elif first == op_role:
                    op_cnt -= 1

        return total

# def evaluate(board: np.ndarray, k: int, role: int) -> int:
#     '''Thuật toán tính heuristic: sliding window kích thước k cho từng hàng, cột và đường chéo'''
#     total = 0
#     m = len(board)
#     n = len(board[0])

#     # Tính điểm các hàng
#     if n >= k:
#         for i in range(m):
#             tmp = evaluate_ln(k, role,
#                               [board[i][j] for j in range(n)])
#             if abs(tmp) == WIN_PTS:
#                 return tmp
#             total += tmp

#     # Tính điểm các cột
#     if m >= k:
#         for j in range(n):
#             tmp = evaluate_ln(k, role,
#                               [board[i][j] for i in range(m)])
#             if abs(tmp) == WIN_PTS:
#                 return tmp
#             total += tmp

#     # Tính điểm các đường chéo xuống từ trái sang i - j = c
#     for c in range(- n + 1, m - 1):
#         # Ta có: 0 <= i < m && i = j + c && 0 <= j < n
#         # Suy ra: 0 <= j + c < m && 0 <= j < n
#         low = max(0, -c)
#         upper = min(m - c, n)
#         if upper - low >= k:
#             tmp = evaluate_ln(k, role,
#                               [board[j + c][j] for j in range(low, upper)])
#             if abs(tmp) == WIN_PTS:
#                 return tmp
#             total += tmp

#     # Tính điểm các đường chéo lên từ trái sang i + j = c
#     for c in range(0, m + n - 1):
#         # Ta có: 0 <= i < m && i = c - j && 0 <= j < n
#         # Suy ra: 0 <= c - j < m && 0 <= j < n
#         # Suy ra: c - m < j && j <= c && 0 <= j < n
#         low = max(0, c - m + 1)
#         upper = min(c + 1, n)
#         if upper - low >= k:
#             tmp = evaluate_ln(k, role,
#                               [board[c - j][j] for j in range(low, upper)])
#             if abs(tmp) == WIN_PTS:
#                 return tmp
#             total += tmp

#     return total


# def evaluate_ln(k: int, role: int, ln):
#     total = 0
#     window = deque(maxlen=k)    # window: một dãy k ô liên tiếp
#     # đếm sl các ô của mỗi bên trong window
#     self_cnt: int = 0
#     op_cnt: int = 0
#     op_role = getOp(role)

#     # Duyệt từng ô
#     for cell in ln:
#         # Thêm ô tiếp theo vào cuối window
#         window.append(cell)
#         if cell == role:
#             self_cnt += 1
#         elif cell == op_role:
#             op_cnt += 1

#         if len(window) == k:
#             # Đánh giá window
#             if self_cnt > 0:
#                 if op_cnt == 0:         # Khi window chứa ô của bên mình và không chứa ô của đối thủ
#                     if self_cnt == k:   # Thắng
#                         return WIN_PTS
#                     else:
#                         # Công thức tính điểm của window cho bên mình: 2^(EXP * số ô bên mình)
#                         total += 1 << (EXP * (self_cnt - 1))
#             elif op_cnt > 0:            # Khi window chứa ô của đối thủ và không chứa ô của bên mình
#                 if op_cnt == k:         # Thua
#                     return -WIN_PTS
#                 else:
#                     # Công thức tính điểm của window cho đối thủ: 2^(EXP * số ô đối thủ)
#                     total -= 1 << (EXP * (op_cnt - 1))

#             # loại bỏ phần tử đầu khi window đã đạt đủ kích thước k
#             first = window.popleft()
#             if first == role:
#                 self_cnt -= 1
#             elif first == op_role:
#                 op_cnt -= 1

#     return total
