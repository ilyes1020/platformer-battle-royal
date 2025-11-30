import serial
import sys
import platform
import time

# --- OS DETECTION AND LIBRARY SELECTION ---
if platform.system() == 'Windows':
    try:
        import pydirectinput as controller  # Use pydirectinput on Windows
    except ImportError:
        print("Error: Please install 'pydirectinput' (see requirements_joystick.txt)")
        sys.exit()
    default_port = 'COM4' # Change this to your Arduino port on Windows
else:
    try:
        import pyautogui as controller      # Use pyautogui on Linux/Mac
    except ImportError:
        print("Error: Please install 'pyautogui' (see requirements_joystick.txt)")
        sys.exit()
    default_port = '/dev/ttyACM0'           # Default port on Linux

# --- SERIAL CONNECTION ---
try:
    arduino = serial.Serial(default_port, 9600, timeout=.1)     #serial input from arduino. change COM port to wherever your arduino is connected
except serial.SerialException:
    # If default port fails on Linux, try the secondary common port
    if platform.system() != 'Windows':
        try:
            arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
        except:
            print(f"Error: Arduino not found on {default_port} or /dev/ttyUSB0")
            sys.exit()
    else:
        print(f"Error: Arduino not found on {default_port}")
        sys.exit()

controller.PAUSE = 0

keysDown = {}   #list of currently pressed keys


def keyDown(key):               #what to do if key pressed. takes value from handleJoyStickAsArrowKeys
    keysDown[key] = True        #adds key to KeysDown list
    controller.keyDown(key)     #runs controller (pydirectinput/pyautogui) using key from (argument)
    #print('Down: ', key)       #remove '#' from print to test data stream


def keyUp(key):                     #what to do if key released. takes value from handleJoyStickAsArrowKeys
    if key in keysDown:
        del (keysDown[key])         #remove key from KeysDown
        controller.keyUp(key)       #runs controller (pydirectinput/pyautogui) using key from (argument)
        #print('Up: ', key)         #remove '#' from print to test data stream


def handleJoyStickAsArrowKeys(x, y, z, t):      #note that the x and y directions are swapped due to the way I orient my thumbstick
    if x == 0:          #0 is up on joystick
        keyDown('up')   #add up key to keyDown (argument)
        keyUp('down')   #add down key to keyUp (argument), as you can't press up and down together
    elif x == 2:        #2 is down on joystick
        keyDown('down')
        keyUp('up')
    else:               #1 is neutral on joystick
        keyUp('up')
        keyUp('down')

    if y == 2:          #2 is right on joystick
        keyDown('right')
        keyUp('left')
    elif y == 0:        #0 is left on joystick
        keyDown('left')
        keyUp('right')
    else:               #1 is neutral on joystick
        keyUp('left')
        keyUp('right')

    if z == 1:          #z argument is JSButton in this case. 1 is button pressed
        # Note: 'return' is sometimes issues on Linux/Mac with some libs, 'enter' is safer universally
        keyDown('enter')    #key to be pressed with Joystick button. Change to any key
    else:
        keyUp('enter')      #0 is button not pressed

    if t == 0:
        keyDown('space')
    else:
        keyUp("space")

print(f"Joystick connected on {arduino.port}. Press Ctrl+C to quit.")

while True:
    try:
        rawdata = arduino.readline()            #read serial data from arduino one line at a time
        # Added .strip() to clean hidden characters (CR/LF) that cause bugs on Linux
        data = str(rawdata.decode('utf-8')).strip()     #decode the raw byte data into UTF-8
        
        if data.startswith("S") and len(data) >= 7:    #make sure the read starts in the correct place (+ length check)
            dx = int(data[1])                   #X direction is second digit in data (data[0] is 'S')
            dy = int(data[3])                   #Y direction is fourth digit in data
            JSButton = int(data[5])             #JSButton is sixth digit in data
            Button = int(data[7]) 
            #print(dx, dy, JSButton,Button)            #remove '#' from print to test data stream
            handleJoyStickAsArrowKeys(dx, dy, JSButton, Button)     #run body of code using dx, dy and JSButton as inputs
    except ValueError:
        pass
    except KeyboardInterrupt:
        break