from result import Result

class Minimax:
    def __init__(self, game) -> None:
        self.game = game

    def MAX(self, state):
        if self.game.is_end(state, self.game.player1):
            return self.game.utility(state, self.game.player1)

        v = float("-inf")
        x, y = -1, -1
        for action in self.game.actions(state, self.game.player1):
            res = self.MIN(action.state)
            if res.value > v:
                v = res.value
                x = action.x
                y = action.y

        return Result(v, x, y)

    def MIN(self, state):
        if self.game.is_end(state, self.game.player2):
            return self.game.utility(state, self.game.player2)

        v = float("inf")
        x, y = -1, -1
        for action in self.game.actions(state, self.game.player2):
            res = self.MAX(action.state)
            if res.value < v:
                v = res.value
                x = action.x
                y = action.y

        return Result(v, x, y)
