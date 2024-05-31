from TicTacToeAi import TicTacToeAi
from heuristic import evaluate
from win_lose import can_lose
import numpy as np
from util import toCell


def main():
    board = [
        ['x', 'x', 'x', 'o', 'x'],
        ['x', 'o', ' ', 'o', 'o'],
        ['x', ' ', 'x', 'o', 'o'],
        ['x', 'x', ' ', 'o', 'o'],
        ['x', ' ', 'o', 'x', 'o'],
    ]
    board = [[' ' for i in range(6)] for j in range(6)]
    board[0][0] = 'o'
    ai = TicTacToeAi(5, 'x', max_depth=2)
    move = ai.get_move(board)
    print(can_lose(board, 5, toCell('x')))
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
    print(f'Complexity: {ai.cnt * len(board) * len(board[0])}')
    print(f'Searched nodes: {ai.cnt}')
    print(f'Pruned nodes: {ai.prune}')
    print(f'Pruning rate: {ai.get_prune_rate()}')

if __name__ == "__main__":
    main()
