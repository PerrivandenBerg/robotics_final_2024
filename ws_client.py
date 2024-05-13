import asyncio
import websocket
import threading
from time import sleep

class RobotWebSocketConnection:

    ws: websocket.WebSocket

    def __init__(self):
        self.ws = websocket.WebSocket()
        self._connect()
        print('Connected to robot websocket server')

    def _connect(self):
        self.ws.connect("ws://localhost:8765")

    # Where command is one of: 'forward', 'backward', 'stop', 'left', or 'right'
    def send_command(self, command: str):
        print('Sending command', command)

        attempts = 3
        while attempts > 0:
            try:
                self.ws.send_text(command)
                return
            except Exception as e:
                print('error:', e, type(e))
                attempts -= 1
                print(f'trying to reconnect (attempt {3 - attempts})')
                self._connect()
        print('Could not reconnect. Exiting.')
        exit(1)

if __name__ == '__main__':
    robot_ws = RobotWebSocketConnection()
    robot_ws.send_command('left')
    sleep(1000)