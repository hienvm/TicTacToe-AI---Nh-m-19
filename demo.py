from time import perf_counter
from TicTacToeAi import TicTacToeAi
from heuristic import evaluate
from static_check import can_lose
import numpy as np
from util import toCell


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

    begin = perf_counter()
    for i in range(1):
        move = ai.get_move(board)
    end = perf_counter()
    print(f"Time: {end - begin}")
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
        
    # print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    print(f'Searched nodes: {ai.cnt}')
    print(f'Pruned nodes: {ai.prune}')
    # 7x7 +2: cnt=461 prune=99029 0.3s
    # 7x7 +4: cnt=101879 prune=244617798 72s
    # 15x15 +2: cnt=4244 prune=10837800 19s
    # print(f'Pruning rate: {ai.get_prune_rate()}')

if __name__ == "__main__":
    main()
