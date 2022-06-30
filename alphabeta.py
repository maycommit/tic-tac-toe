from result import Result

class Alphabeta:
    def __init__(self, game) -> None:
        self.game = game

    def MAX(self, state, alpha = float("-inf"), beta = float("inf")):
        if self.game.is_end(state, self.game.player1):
            return self.game.utility(state, self.game.player1)

        v = float("-inf")
        x, y = -1, -1
        for action in self.game.actions(state, self.game.player1):
            res = self.MIN(action.state, alpha, beta)
            if res.value > v:
                v = res.value
                x = action.x
                y = action.y

            if v >= beta:
                return Result(v, x, y)

            alpha = max(alpha, v)

        return Result(v, x, y)

    def MIN(self, state, alpha = float("-inf"), beta = float("inf")):
        if self.game.is_end(state, self.game.player2):
            return self.game.utility(state, self.game.player2)

        v = float("inf")
        x, y = -1, -1
        for action in self.game.actions(state, self.game.player2):
            res = self.MAX(action.state, alpha, beta)
            if res.value < v:
                v = res.value
                x = action.x
                y = action.y

            if v <= alpha:
                return Result(v, x, y)

            beta = min(beta, v)

        return Result(v, x, y)
