from TicTacToeAi import TicTacToeAi
from static_check import can_lose
import numpy as np
from util import toCell
from time import perf_counter_ns
from heuristic import Heuristic
import numpy.random as random

def main():
    board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'x', 'x', ' ', 'o', ' '],
        [' ', ' ', 'x', 'x', ' ', 'o', ' '],
        [' ', ' ', ' ', ' ', ' ', 'o', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    board = [[' ' for i in range(15)] for j in range(15)]
    board[0][0] = 'o'

    ai = TicTacToeAi(5, 'x', max_depth=2)

    begin = perf_counter_ns()
    for i in range(1):
        move = ai.get_move(board)
    end = perf_counter_ns()
    print(f"Time: {end - begin}")
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')

    print(100732387800 / 17009103400)
    print(18630419700 / 16415071000)

    # begin = perf_counter_ns()
    # for i in range(10000):
    #     r = h.sum()
    # end = perf_counter_ns()
    # print(end - begin)

    # print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    # print(f'Searched nodes: {ai.cnt}')
    # print(f'Pruned nodes: {ai.prune}')
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
