import asyncio
import websockets
from alphabeta import Alphabeta
import event
import json
import copy
from game import Game
from minimax import Minimax

player1, player2 = 'X', 'O'
initial_state = [["", "", ""], ["", "", ""], ["", "", ""]]

class Server:
    def __init__(self) -> None:
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player = player1
        self.game = Game(player1, player2)


    def is_finished(self):
        if self.game.is_win(self.state, player1):
            return player1
        if self.game.is_win(self.state, player2):
            return player2
        if self.game.is_tie(self.state):
            return ''

        return None

    def reset_game(self):
        self.player = player1
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]


    def find_next_max_move(self, algorithm, curr_player):
        v = float("-inf")
        cx, cy = 0, 0

        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                if self.state[x][y] == "":
                    self.state[x][y] = curr_player
                    minimax_val = algorithm.MAX(copy.deepcopy(self.state))
                    self.state[x][y] = ""

                    if minimax_val > v:
                        cx, cy = x, y
                        v = minimax_val

        return cx, cy

    def find_next_min_move(self, algorithm, curr_player):
        v = float("inf")
        cx, cy = 0, 0

        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                if self.state[x][y] == "":
                    self.state[x][y] = curr_player
                    minimax_val = algorithm.MIN(copy.deepcopy(self.state))
                    self.state[x][y] = ""

                    if minimax_val < v:
                        cx, cy = x, y
                        v = minimax_val
        return cx, cy


    async def handler(self, websocket):
        while True:
            await websocket.send(event.start_event())
            message = await websocket.recv()
            menu = json.loads(message)

            algorithm = Minimax(self.game)
            if menu["algorithm"] == 1:
                algorithm = Alphabeta(self.game)

            while True:
                winner = self.is_finished()
                if winner != None:
                    await websocket.send(event.winner_event(winner))
                    self.reset_game()
                    break

                if self.player == player1:
                    x, y = 0, 0
                    if menu["option"] == 1:
                        message = await websocket.recv()
                        coord = json.loads(message)
                        x, y = coord["x"], coord["y"]
                    else:
                        x, y = self.find_next_max_move(algorithm, player1)
                        await websocket.send(event.movement_event(player1,x,y))

                    self.state[x][y] = player1
                    self.player = player2

                else:
                    x, y = 0, 0
                    if menu["option"] == 2:
                        message = await websocket.recv()
                        coord = json.loads(message)
                        x, y = coord["x"], coord["y"]
                    else:
                        x, y = self.find_next_min_move(algorithm, player2)
                        await websocket.send(event.movement_event(player2,x,y))

                    self.state[x][y] = player2
                    self.player = player1

            await websocket.recv()

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()  # run forever

s = Server()
asyncio.run(s.main())
