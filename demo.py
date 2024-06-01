from time import perf_counter_ns
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

    ai = TicTacToeAi(5, 'x', max_depth=4)

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
    # print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    # print(f'Searched nodes: {ai.cnt}')
    # print(f'Pruned nodes: {ai.prune}')
    # print(f'Pruning rate: {ai.get_prune_rate()}')

if __name__ == "__main__":
    main()
