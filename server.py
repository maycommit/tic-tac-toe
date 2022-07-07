import asyncio
import websockets
from alphabeta import Alphabeta
import event
import json
from game import Game
from minimax import Minimax

initial_state = [["", "", ""], ["", "", ""], ["", "", ""]]

class Server:
    def __init__(self) -> None:
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player = Game.player1
        self.game = Game()


    def is_finished(self):
        if self.game.winner(self.state, Game.player1):
            return Game.player1
        if self.game.winner(self.state, Game.player2):
            return Game.player2
        if self.game.is_tie(self.state):
            return ''

        return None

    def reset_game(self):
        self.player = Game.player1
        self.state = [["", "", ""], ["", "", ""], ["", "", ""]]
    
    def is_first_move(self):
        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                if self.state[x][y] != "":
                    return False
        
        return True
    
    async def player1_play(self, websocket, menu, algorithm):
        x, y = 0, 0
        if menu["option"] == 1:
            message = await websocket.recv()
            coord = json.loads(message)
            x, y = coord["x"], coord["y"]
        else:
            if self.is_first_move():
                x, y = self.game.random_play()
            else:
                x, y = algorithm.max_movement(self.state)
            
            await websocket.send(event.movement_event(Game.player1,x,y))
        
        return x, y
    
    async def player2_play(self, websocket, menu, algorithm):
        x, y = 0, 0
        if menu["option"] == 2:
            message = await websocket.recv()
            coord = json.loads(message)
            x, y = coord["x"], coord["y"]
        else:
            x, y = algorithm.min_movement(self.state)
            await websocket.send(event.movement_event(Game.player2,x,y))
        
        return x, y


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

                if self.player == Game.player1:
                    x, y = await self.player1_play(websocket, menu, algorithm)
                    self.state[x][y] = Game.player1
                    self.player = Game.player2
                else:
                    x, y = await self.player2_play(websocket, menu, algorithm)
                    self.state[x][y] = Game.player2
                    self.player = Game.player1

            await websocket.recv()

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()  # run forever

s = Server()
asyncio.run(s.main())
