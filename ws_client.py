import asyncio
import websocket
import threading
from time import sleep

class RobotWebSocketConnection:
    ws: websocket.WebSocketApp
    t: threading.Thread

    def __init__(self):
        self.ws = websocket.WebSocketApp('ws://localhost:8765', on_message=print, on_error=print)
        self.t = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.t.start()
        sleep(0.1)
        print('Connected to robot websocket server')

    # Where command is one of: 'forward', 'backward', 'stop', 'left', or 'right'
    def send_command(self, command: str):
        print('Sending command', command)
        self.ws.send_text(command)

if __name__ == '__main__':
    robot_ws = RobotWebSocketConnection()
    robot_ws.send_command('left')
    sleep(1000)