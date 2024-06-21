# Robotics Final Assignment

## Setup
### Windows PC with WSL
1. Update linux to get the "+" from the following: https://askubuntu.com/questions/1405903/capturing-webcam-video-with-opencv-in-wsl2
2. Connect camera to linux via powershell.
 - Open "cmd" and type "usbipd list".
 - Find the BUSID of the webcam.
 - usbipd attach --wsl --busid=<BUSID>
 - "usbipd list" should now say "Attached".
 - Open linux and type "sudo chmod 777 /dev/video0".
4. Make an enviroment and install requirements.
### Robot
1. Copy ws_server.py to the robot and run on the robot when running detect.py on the Windows PC.

## How to record gestures
1. Have a hand gesture ready infront of your camera.
2. Run the record.py file.
3. Hold the gesture infront of the camera while moving it around and tweaking
your fingers bit by bit. (The program will take an average of the whole measurement)
4. After ~10s the program stops and outputs the gesture configuration.
5. Copy paste the output into the detect.py file, and add to the gesture list. Examples for gestures are already present in the file.

## How to detect
0. Make sure to connect to the robot via wifi.
1. Run the detect.py file on the PC and run ws_server.py on the robot.
2. Make a gesture (out of the list in detect.py) and it should work accordingly.
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
