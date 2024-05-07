from TicTacToeAi import TicTacToeAi
from heuristic import evaluate
from win_lose import can_lose


def main():
    board = [
        ['x', 'o', 'x', 'x', 'x'],
        ['x', 'o', 'x', 'o', 'x'],
        [' ', 'o', 'x', 'o', 'x'],
        ['o', 'o', 'o', 'o', 'x'],
        ['o', 'x', 'o', 'x', 'x'],
    ]
    ai = TicTacToeAi(5, 'x')
    move = ai.get_move(board)
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
    print(f'Complexity: {ai.cnt * 25}')
    print(f'Pruned nodes: {ai.prune}')
    print(can_lose(board, 5, 'x'))
    print(f'Pruning rate: {ai.get_prune_rate()}')

if __name__ == "__main__":
    main()
