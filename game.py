import copy
import random
from action import Action
from result import Result

class Game:
    player1 = 'X'
    player2 = 'O'
    tie = "tie"

    def is_tie(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == "":
                    return False

        return True

    def winner(self, state, player):
        for i in range(len(state)):
            if state[i][0] == player and state[i][1] == player and state[i][2] == player:
                return True

            if state[0][i] == player and state[1][i] == player and state[2][i] == player:
                return True

        if state[0][0] == player and state[1][1] == player and state[2][2] == player:
            return True

        if state[0][2] == player and state[1][1] == player and state[2][0] == player:
            return True

    def is_end(self, state, player):
        return self.is_win(state, player) or self.is_tie(state)

    def random_play(self):
        positions = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2],
        ]

        i = random.randint(0, len(positions) - 1)
        x, y = positions[i]
        return x, y

    def human_play(self):
        print("Digite as coordenadas:")
        x, y = input().split()
        return Result(-1, int(x), int(y))

    def print(self, state):
        for i in range(len(state)):
            print(state[i])
        print()
