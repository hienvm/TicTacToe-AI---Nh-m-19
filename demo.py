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
        [' ', 'x', ' ', ' ', 'o', ' ', ' '],
        [' ', ' ', ' ', ' ', 'o', ' ', ' '],
        [' ', 'x', ' ', ' ', 'o', ' ', ' '],
        [' ', 'x', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    ai = TicTacToeAi(5, 'x', max_depth=4)
    move = ai.get_move(board)
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
    # print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    # print(f'Searched nodes: {ai.cnt}')
    # print(f'Pruned nodes: {ai.prune}')
    # print(f'Pruning rate: {ai.get_prune_rate()}')

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
