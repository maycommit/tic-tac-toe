import asyncio
import websockets
import event
import json
from game import Game
from minimax import Minimax


player1, player2 = 'X', 'O'
initial_state = [["", "", ""], ["", "", ""], ["", "", ""]]

class Server:
    def __init__(self) -> None:
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player = player1
        self.game = Game(player1, player2)
        self.algorithm = Minimax(self.game)


    def is_finished(self):
        if self.game.is_win(self.state, player1):
            return player1
        if self.game.is_win(self.state, player2):
            return player2
        if self.game.is_tie(self.state):
            return ''

        return None

    def reset_game(self):
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]


    async def handler(self, websocket):
        while True:
            winner = self.is_finished()
            if winner != None:
                await websocket.send(event.winner_event(winner))
                self.reset_game()

            if self.player == player1:
                message = await websocket.recv()
                coord = json.loads(message)
                self.state[coord["x"]][coord["y"]] = player1
                self.player = player2
            else:
                coord = self.algorithm.MIN(self.state)
                self.state[coord.x][coord.y] = player2
                self.player = player1
                await websocket.send(event.movement_event(player2, coord.x, coord.y))

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()  # run forever

s = Server()
asyncio.run(s.main())
