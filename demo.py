from TicTacToeAi import TicTacToeAi
from heuristic import evaluate
from win_lose import can_lose


def main():
    board = [
        ['x', 'o', 'x', ' ', 'x'],
        [' ', ' ', 'x', 'o', ' '],
        ['o', 'x', 'x', 'o', 'x'],
        [' ', 'x', 'o', 'o', ' '],
        ['o', 'x', 'o', 'x', ' '],
    ]
    ai = TicTacToeAi(5, 'x')
    move = ai.get_move(board)
    print(can_lose(board, 5, 'x'))
    if move is not None:
        print(move)
        board[move[0]][move[1]] = 'x'
    for row in board:
        print('|' + '|'.join([f'{cell}' for cell in row]) + '|')
    print(f'Complexity: {ai.cnt * 25}')
    print(f'Searched nodes: {ai.cnt}')
    print(f'Pruned nodes: {ai.prune}')
    print(f'Pruning rate: {ai.get_prune_rate()}')

if __name__ == "__main__":
    main()
