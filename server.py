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
        self.state = initial_state
        self.player = player1
        self.game = Game(player1, player2)
        self.algorithm = Minimax(self.game)


    def is_finished(self):
        if self.game.is_win(self.state, player1):
            print("Player 1 wins!")
            return True
        if self.game.is_win(self.state, player2):
            print("Player 2 wins!")
            return True
        if self.game.is_tie(self.state):
            print("Is a tie :(")
            return True

        return False


    async def handler(self, websocket):
        while True:
            if self.is_finished():
                websocket.send(event.winner_event(self.player))
                self.state = initial_state

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
