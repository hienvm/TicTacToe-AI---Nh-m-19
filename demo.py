from TicTacToeAi import TicTacToeAi
from heuristic import evaluate


def main():
    board = [
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
    ]
    ai = TicTacToeAi(board, 5, 'x')
    print(ai.get_move())
    print(ai.get_prune_rate())


if __name__ == "__main__":
    main()
