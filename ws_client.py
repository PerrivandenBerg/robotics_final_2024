import asyncio
import websocket
import threading
from time import sleep

class RobotWebSocketConnection:

    ws: websocket.WebSocket

    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://localhost:8765")
        print('Connected to robot websocket server')
        

    # Where command is one of: 'forward', 'backward', 'stop', 'left', or 'right'
    def send_command(self, command: str):
        print('Sending command', command)
        self.ws.send_text(command)


if __name__ == '__main__':
    robot_ws = RobotWebSocketConnection()
    robot_ws.send_command('left')
    sleep(1000)