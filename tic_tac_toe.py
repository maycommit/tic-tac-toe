from game import Game
from minimax import Minimax
from alphabeta import Alphabeta

class TicTacToe:
    def __init__(self) -> None:
        self.player1 = 'X'
        self.player2 = 'O'
        self.board = None
        self.current_player = None
        self.game = Game(self.player1, self.player2)
        self.algorithm = Alphabeta(self.game)

    def init_game(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.current_player = self.player1

    def is_finished(self):
        if self.game.is_win(self.board, self.player1):
            print("Player 1 wins!")
            return True
        if self.game.is_win(self.board, self.player2):
            print("Player 2 wins!")
            return True
        if self.game.is_tie(self.board):
            print("Is a tie :(")
            return True

        return False


    def menu(self):
        print("==========")
        print("1 - H vs M")
        print("2 - M vs H")
        print("3 - M vs M")
        print("0 - Sair")
        print("==========")
        return int(input())

    def start(self):
        while True:
            self.init_game()
            menu = self.menu()
            if menu == 0:
                break

            while True:
                if self.is_finished():
                    break

                res = None
                if self.current_player == self.player1:
                    res = self.game.human_play() if menu == 1 else self.algorithm.MAX(self.board)
                    self.board[res.x][res.y] = self.player1
                    self.current_player = self.player2
                else:
                    res = self.game.human_play() if menu == 2 else self.algorithm.MIN(self.board)
                    self.board[res.x][res.y] = self.player2
                    self.current_player = self.player1

                self.game.print(self.board)

