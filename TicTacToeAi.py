from collections import deque
from typing import Literal
import numpy as np
import multiprocessing as mp

from heuristic import evaluate
from util import INF, WIN_PTS, Cell, getOp, toCell
from static_check import can_lose

# TODO
# chạy đa luồng cho tầng đầu tiên
# check nhanh thắng thua trong O(1)
# dùng queue để lưu trữ các nc đi khả thi
# (done) khắc phục tình trạng đánh bi quan, ko tận dụng nốt cơ hội khi nước đi tốt nhất chỉ dẫn đến hòa (có thể bằng cách giảm MAX_DEPTH nếu biết ko thể thua)

MAX_DEPTH = 2

class TicTacToeAi:
    def __init__(self, k: int, role: str | int, max_depth=MAX_DEPTH) -> None:
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

        # self.prune = 0
        # self.cnt = 0

        if role in (Cell.X, Cell.O):
            self.role = role
        elif role in ("x", "X"):
            self.role = Cell.X
        else:
            self.role = Cell.O
        self.op_role = getOp(self.role)

        # self.state = 1 << (self.m * self.n * 2)
        # self.available_moves = deque(maxlen=m*n)

    def get_move(self, board: list[list[str]]) -> tuple[int, int] | None:
        self.board = np.array([[toCell(s) for s in row]
                              for row in board], dtype=np.uint8)
        self.m = len(self.board)
        self.n = len(self.board[0])
        # self.prune = 0

        # self.cnt += 1

        if self.board.sum() == 0:
            return (int(self.m / 2), int(self.n / 2))

        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role)
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
                
                
        print(self.board)
        print(res[0])
        
        return res[0]

    def search_best_move_parallel(self) -> tuple[tuple[int, int], int] | None:
        # self.cnt += 1
        # beta = INF
        tasks = []
        processes = []
        alpha = mp.Value('i', -INF)
        move = None
        val = mp.Value('i', -INF)
        movei = mp.Value('i', -1)
        movej = mp.Value('i', -1)
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == Cell.EMPTY:
                    tasks.append((i, j, self.k, self.role,
                                  self.max_depth, self.board, alpha, val, movei, movej))

        for task in tasks:
            p = mp.Process(target=proccess_depth1, args=task)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        if movei.value >= 0 and movej.value >= 0:
            move = (movei.value, movej.value)

        if move is None:
            return None

        return (move, val.value)

    def search_best_move(self) -> tuple[tuple[int, int], int] | None:
        # self.cnt += 1

        move = None
        val = -INF
        alpha = -INF
        beta = INF

        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == Cell.EMPTY:
                    # Duyệt backtrack cây con
                    self.board[i][j] = self.role
                    tmp = self.search_min(alpha, beta, 1)
                    self.board[i][j] = Cell.EMPTY

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
        # self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role)
        if abs(stop) == WIN_PTS:
            return stop

        val = -INF
        is_leaf = True

        if depth < self.max_depth:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == Cell.EMPTY:
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.role
                        tmp = self.search_min(alpha, beta, depth + 1)
                        self.board[i][j] = Cell.EMPTY

                        if tmp > val:
                            val = tmp
                            if val > alpha:
                                alpha = val
                            if val >= beta:
                                # self.prune += (self.m * self.n -
                                #                depth) ** (self.max_depth - depth - 1)
                                # print("prune_max")
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    def search_min(self, alpha, beta, depth) -> int:
        # self.cnt += 1
        # Check thắng thua, có thể cải thiện cách tính
        stop = evaluate(self.board, self.k, self.role)
        if abs(stop) == WIN_PTS:
            return stop

        val = INF
        is_leaf = True

        if depth < self.max_depth:
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == Cell.EMPTY:
                        is_leaf = False

                        # Duyệt backtrack cây con
                        self.board[i][j] = self.op_role
                        tmp = self.search_max(alpha, beta, depth + 1)
                        self.board[i][j] = Cell.EMPTY

                        if tmp < val:
                            val = tmp
                            if val < beta:
                                beta = val
                            if val <= alpha:
                                # self.prune += (self.m * self.n -
                                #                depth) ** (self.max_depth - depth + 1) - 1
                                # print("prune_min")
                                return val

        # Nếu là lá (không còn nc đi hoặc chạm đáy) thì đánh giá heuristic
        if is_leaf:
            return stop

        return val

    # def get_prune_rate(self):
    #     '''Tính tỉ lệ cắt tỉa.\n
    #     Có thể chỉnh cách tính pruning cho chính xác hơn.'''
    #     return float(self.prune) / (self.cnt + self.prune)


def proccess_depth1(i, j, k, role, max_depth, board, alpha, val, movei, movej):
    ai = TicTacToeAi(k, role, max_depth)
    ai.board = board
    ai.m = len(board)
    ai.n = len(board[0])
    # Duyệt backtrack cây con
    board[i][j] = role
    tmp = ai.search_min(alpha=alpha.value, beta=INF, depth=1)
    board[i][j] = Cell.EMPTY
    if tmp > val.value:
        val.value = tmp
        if tmp > alpha.value:
            alpha.value = tmp
        movei.value = i
        movej.value = j
