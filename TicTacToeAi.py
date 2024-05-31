from collections import deque
from typing import Literal
import numpy as np

from heuristic import evaluate
from util import INF, WIN_PTS
from win_lose import can_lose

# TODO
# chạy đa luồng cho tầng đầu tiên
# check nhanh thắng thua trong O(1)
# dùng queue để lưu trữ các nc đi khả thi
# (done) khắc phục tình trạng đánh bi quan, ko tận dụng nốt cơ hội khi nước đi tốt nhất chỉ dẫn đến hòa (có thể bằng cách giảm MAX_DEPTH nếu biết ko thể thua)

MAX_DEPTH = 1

class TicTacToeAi:
    def __init__(self, k: int, role: Literal['x', 'o'], max_depth=MAX_DEPTH) -> None:
        """
        Args:
            k (int): Số ô liên tiếp cần để thắng
            role (str): 'x' | 'o'
        """
        self.board: np.ndarray
        self.m = 0
        self.n = 0
        self.k = k
        self.max_depth = max_depth

        self.prune = 0
        self.cnt = 0

        self.role: Literal['x', 'o'] = role
        self.op_role: Literal['x', 'o'] = "x"
        if role == "x":
            self.op_role = "o"

        # self.state = 1 << (self.m * self.n * 2)
        # self.available_moves = deque(maxlen=m*n)

    def get_move(self, board: list[list[str]]) -> tuple[int, int] | None:
        self.board = np.array(board)
        self.m = len(board)
        self.n = len(board[0])
        self.prune = 0

        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return None

        res = self.search_best_move()

        if res is None:
            return None

        if res[1] == 0 and not can_lose(self.board, self.k, self.role):
            tmp_depth = self.max_depth
            while self.max_depth >= 2:
                if self.max_depth == 2:
                    self.max_depth = 1
                else:
                    self.max_depth -= 2
                tmp_res = self.search_best_move()
                if tmp_res is not None and tmp_res[1] > 0:
                    self.max_depth = tmp_depth
                    return tmp_res[0]

        return res[0]

    def search_best_move(self) -> tuple[tuple[int, int], int] | None:
        self.cnt += 1

        move = None
        val = -INF
        alpha = -INF
        beta = INF

        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == ' ':
                    # Duyệt backtrack cây con
                    self.board[i][j] = self.role
                    tmp = self.search_min(alpha, beta, 1)
                    self.board[i][j] = ' '

                    if tmp > val:
                        val = tmp
                        if val > alpha:
                            alpha = val
                        # if val >= beta:
                        #     return val
                        # Cập nhật nước đi tốt nhất
                        move = (i, j)

        if move is None:
            return None

        return (move, val)

    def search_max(self, alpha, beta, depth) -> int:
        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return stop

        val = -INF
        is_leaf = True

        if depth < self.max_depth:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == ' ':
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.role
                        tmp = self.search_min(alpha, beta, depth + 1)
                        self.board[i][j] = ' '

                        if tmp > val:
                            val = tmp
                            if val > alpha:
                                alpha = val
                            if val >= beta:
                                self.prune += (self. m * self.n -
                                               depth) ** (self.max_depth - depth - 1)
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    def search_min(self, alpha, beta, depth) -> int:
        self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role, self.op_role)
        if abs(stop) == WIN_PTS:
            return stop

        val = INF
        is_leaf = True

        if depth < self.max_depth:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == ' ':
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.op_role
                        tmp = self.search_max(alpha, beta, depth + 1)
                        self.board[i][j] = ' '

                        if tmp < val:
                            val = tmp
                            if val < beta:
                                beta = val
                            if val <= alpha:
                                self.prune += (self. m * self.n -
                                               depth) ** (self.max_depth - depth + 1) - 1
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    def get_prune_rate(self):
        '''Tính tỉ lệ cắt tỉa.\n
        Có thể chỉnh cách tính pruning cho chính xác hơn.'''
        return float(self.prune) / (self.cnt + self.prune)
