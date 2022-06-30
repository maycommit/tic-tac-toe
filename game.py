import copy
import random
from action import Action
from result import Result

class Game:
    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2

    def is_tie(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == "":
                    return False

        return True

    def is_win(self, state, player):
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

    def actions(self, state, player):
        a = []
        positions = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2],
        ]

        while len(positions) > 0:
            i = random.randint(0, len(positions) - 1)
            x, y = positions[i]
            if state[x][y] == "":
                state[x][y] = player
                new_state = copy.deepcopy(state)
                new_action = Action(new_state, x, y)
                a.append(new_action)
                state[x][y] = ""

            positions.pop(i)

        return a

    def utility(self, state, player):
        if self.is_win(state, player):
            value = 1.0 if player == self.player1 else 0
            return Result(value, -1, -1)

        if self.is_tie(state):
            return Result(0.5, -1, -1)

    def human_play(self):
        print("Digite as coordenadas:")
        x, y = input().split()
        return Result(-1, int(x), int(y))

    def print(self, state):
        for i in range(len(state)):
            print(state[i])
        print()
