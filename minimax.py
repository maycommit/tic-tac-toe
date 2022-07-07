from result import Result

class Minimax:
    def __init__(self, game) -> None:
        self.game = game

    def MAX(self, state):
        if self.game.is_end(state, self.game.player):
            return self.game.utility(state)

        v = float("-inf")
        for action in self.game.seq_actions(state, self.game.player):
            min_val = self.MIN(action)
            v = max(min_val, v)

        return v

    def MIN(self, state, curr_player):
        if self.game.is_end(state, curr_player, self.game.oponent):
            return self.game.utility(state)

        v = float("inf")
        for action in self.game.seq_actions(state, self.game.oponent):
            max_val = self.MAX(action)
            v = min(max_val, v)

        return v
