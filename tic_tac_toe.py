from game import Game
from minimax import Minimax

class TicTacToe:
    def __init__(self) -> None:
        self.player1 = 'X'
        self.player2 = 'O'
        self.current_player = self.player1
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.game = Game(self.player1, self.player2)
        self.algorithm = Minimax(self.game)

    def is_finished(self):
        if self.game.is_tie(self.board):
            print("Is a tie :(")
            return True
        if self.game.is_win(self.board, self.player1):
            print("Player 1 wins!")
            return True
        if self.game.is_win(self.board, self.player2):
            print("Player 2 wins!")
            return True

        return False


    def start(self):
        while True:
            if self.is_finished():
                break

            res = None
            if self.current_player == self.player1:
                res = self.game.human_play()
                self.board[res.x][res.y] = self.player1
                self.current_player = self.player2
            else:
                res = self.algorithm.MIN(self.board)
                self.board[res.x][res.y] = self.player2
                self.current_player = self.player1

            self.game.print(self.board)

