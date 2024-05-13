# Robotics Final Assignment

## Setup
1. Update linux to get the "+" thingy.
2. Connect camera to linux via powershell.
 - Open "cmd" and type "usbipd list".
 - Find the BUSID of the webcam.
 - usbipd attach --wsl --busid=<BUSID>
 - "usbipd list" should now say "Attached".
 - Open linux and type "sudo chmod 777 /dev/video0".
4. Make an enviroment and install requirements.

## How to record?
1. Have a hand gesture ready infront of your camera.
2. Run the record.py file.
3. Hold the gesture infront of the camera while moving it around and tweaking
your fingers bit by bit.
4. After ~10s the program stops and outputs the gesture configuration.
5. Copy paste this into the detect.py file, and fill in the TODO at the end.

## How to detect?
1. Run the detect.py file.
2. Make a gesture (out of the list) and it should work accordingly.
3. Press 'q' or '^C' to exit.

## Notes
- The software right now only detects the right hand gestures.


# Port forwarding for websockets
Add this to your ssh config for the robot:
```
LocalForward 8765 localhost:8765 
```

Complete example:
```
Host robot
    HostName 10.42.0.1
    User pi
    LocalForward 8765 localhost:8765 
```