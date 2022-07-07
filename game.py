import copy
import random
from action import Action
from result import Result

class Game:
    def __init__(self, player, oponent) -> None:
        self.player = player
        self.oponent = oponent

    def is_tie(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == "":
                    return False

        return True

    def is_win(self, state, curr_player):
        for i in range(len(state)):
            if state[i][0] == curr_player and state[i][1] == curr_player and state[i][2] == curr_player:
                return True

            if state[0][i] == curr_player and state[1][i] == curr_player and state[2][i] == curr_player:
                return True

        if state[0][0] == curr_player and state[1][1] == curr_player and state[2][2] == curr_player:
            return True

        if state[0][2] == curr_player and state[1][1] == curr_player and state[2][0] == curr_player:
            return True

    def is_end(self, state, curr_player):
        return self.is_win(state, curr_player) or self.is_tie(state)

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

    def seq_actions(self, state, curr_player):
        a = []

        for x in range(len(state)):
            for y in range(len(state[x])):
                if state[x][y] == '':
                    state[x][y] = curr_player
                    new_state = copy.deepcopy(state)
                    a.append(new_state)
                    state[x][y] = ''

        return a

    def utility(self, state):
        if self.is_win(state, self.player):
            return 1

        if self.is_win(state, self.oponent):
            return -1

        if self.is_tie(state):
            return 0

    def human_play(self):
        print("Digite as coordenadas:")
        x, y = input().split()
        return Result(-1, int(x), int(y))

    def print(self, state):
        for i in range(len(state)):
            print(state[i])
        print()
