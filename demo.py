from TicTacToeAi import TicTacToeAi
from static_check import can_lose
import numpy as np
from util import toCell
from time import perf_counter_ns, perf_counter
from heuristic import Heuristic
import numpy.random as random

def main():
    board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'o', 'o', 'x', 'o', 'o', ' ', ' '], [' ', ' ', ' ', ' ', 'x', 'o', 'x', ' ', ' ', ' '], [
        ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'x', ' ', 'x', ' ', ' ', ' '], [' ', ' ', ' ', 'x', ' ', ' ', ' ', 'o', ' ', ' '], [' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    board = [
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
        ['x', ' ', ' ', 'x', ' ', ' ', ' ', ' ',],
        [' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ',],
        [' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ',],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    ]

#      , , , , , , , , , ,
#  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,
#  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,
#  ,  ,  , o, o, x, o, o,  ,  ,
#  ,  ,  ,  , x, o, x,  ,  ,  ,
#  ,  ,  ,  ,  , x, x, x,  ,  ,
#  ,  ,  ,  , x,  , x,  ,  ,  ,
#  ,  ,  , x,  ,  , o, o,  ,  ,
#  ,  , o,  ,  ,  ,  ,  ,  ,  ,
#  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,

    # board = [
    #     ['o', ' ', ' ', ' ', 'x'],
    #     [' ', 'x', ' ', 'o', ' '],
    #     ['x', 'x', 'o', 'x', ' '],
    #     [' ', 'o', 'x', 'o', 'x'],
    #     [' ', 'x', ' ', ' ', 'o'],
    # ]

    # board = [[' ' for i in range(15)] for j in range(15)]
    # for i in range(2, 15):
    #     for j in range(15):
    #         if (j + i) % 2:
    #             board[i][j] = 'x'
    #         else:
    #             board[i][j] = 'o'
    # board[0][0] = 'x'

    ai = TicTacToeAi(5, 'o')

    begin = perf_counter()
    for i in range(1):
        move = ai.get_move(board)
    end = perf_counter()
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'o'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
    print(f"Time: {end - begin}")

    # print(100732387800 / 17009103400)
    # print(18630419700 / 16415071000)

    # begin = perf_counter_ns()
    # for i in range(10000):
    #     r = h.sum()
    # end = perf_counter_ns()
    # print(end - begin)

    # print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    # print(f'Searched nodes: {ai.cnt}')
    # print(f'Pruned nodes: {ai.prune}')
    # 7x7 +2: cnt=144 prune=108241 0.5s
    # 7x7 +4: cnt=8449 prune=254484837 28s
    # 15x15 +2: cnt=672 prune=11189025 16s -> parallel 6s
    # print(f'Pruning rate: {ai.get_prune_rate()}')

    # board = np.array([[toCell(s) for s in row]
    #                   for row in board], dtype=np.uint8)
    # h = Heuristic(5, 1)
    # h.build(board)
    # board[2][1] = 1
    # h.update(2, 1)
    # board[4][4] = 2
    # h.update(4, 4)
    # print(board)
    # print(h.sum())
    # h = Heuristic(5, 1)
    # h.build(board)
    # begin = perf_counter_ns()
    # for i in range(10000):
    #     r = h.update(5, 5)
    # end = perf_counter_ns()
    # print(end - begin)

    # begin = perf_counter_ns()
    # for i in range(10000):
    #     r = h.sum()
    # end = perf_counter_ns()
    # print(end - begin)



if __name__ == "__main__":
    main()
