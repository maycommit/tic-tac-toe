import copy
from game import Game

class Alphabeta:
    def __init__(self, game: Game) -> None:
        self.game = game
    
    def max_movement(self, state):
        mx, my = -1, -1
        v = float("-inf")

        for x in range(len(state)):
            for y in range(len(state[x])):
                if state[x][y] == "":
                    state[x][y] = Game.player1
                    new_state = copy.deepcopy(state)
                    max_val = self.__MIN(new_state)
                    state[x][y] = ""

                    if max_val > v:
                        v = max_val
                        mx, my = x, y
        
        return mx, my
    
    def min_movement(self, state):
        mx, my = -1, -1
        v = float("inf")

        for x in range(len(state)):
            for y in range(len(state[x])):
                if state[x][y] == "":
                    state[x][y] = Game.player2
                    new_state = copy.deepcopy(state)
                    res = self.__MAX(new_state)
                    state[x][y] = ""

                    if res < v:
                        v = res
                        mx, my = x, y
        
        return mx, my
    
    def __actions(self, state, player):
        a = []

        for x in range(len(state)):
            for y in range(len(state[x])):
                if state[x][y] == "":
                    state[x][y] = player
                    new_state = copy.deepcopy(state)
                    a.append(new_state) 
                    state[x][y] = ""
        return a

    def __utility(self, player):
        return {
            Game.player1: 1,
            Game.player2: -1,
            Game.tie: 0,
        }[player]

    def __terminal(self, state):
        if self.game.winner(state, Game.player1):
            return Game.player1
        
        if self.game.winner(state, Game.player2):
            return Game.player2
        
        if self.game.is_tie(state):
            return Game.tie
        
        return False
    
    def __opposite_player(self, player):
        return Game.player2 if player == Game.player1 else Game.player1

    def __MAX(self, state, player=Game.player1, alpha = float("-inf"), beta = float("inf")):
        terminal_val = self.__terminal(state)
        if terminal_val:
            utility = self.__utility(terminal_val)
            return utility

        v = float("-inf")
        for action in self.__actions(state, player):
            v = max(v, self.__MIN(action, self.__opposite_player(player), alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)

        return v

    def __MIN(self, state, player=Game.player2, alpha = float("-inf"), beta = float("inf")):
        terminal_val = self.__terminal(state)
        if terminal_val:
            utility = self.__utility(terminal_val)
            return utility

        v = float("inf")
        for action in self.__actions(state, player):
            v = min(v, self.__MAX(action, self.__opposite_player(player), alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)

        return v

