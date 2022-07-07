import asyncio
import websockets
from alphabeta import Alphabeta
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
    
    def is_first_move(self):
        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                if self.state[x][y] != "":
                    return False
        
        return True



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
                        if self.is_first_move():
                            x, y = self.game.random_play()
                        else:
                            coord = algorithm.MAX(self.state)
                            x, y = coord.x, coord.y
                        
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
                        coord = algorithm.MIN(self.state)
                        x, y = coord.x, coord.y
                        await websocket.send(event.movement_event(player2,x,y))

                    self.state[x][y] = player2
                    self.player = player1

            await websocket.recv()

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()  # run forever

s = Server()
asyncio.run(s.main())
