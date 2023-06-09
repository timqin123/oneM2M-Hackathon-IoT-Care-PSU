import threading
from pynput import keyboard
from gpiozero import LineSensor
import time
import atexit
import globalVars


sensorLeft = None
sensorRight = None
threshold = 0.5


def autoDriveThreadFunc():
	while not globalVars.quitFlagAutoDrive:
		valLeft=sensorLeft.value
		valRight=sensorRight.value
		key = None
		if valLeft > threshold:
			key = keyboard.Key.left
		elif valRight > threshold:
			key = keyboard.Key.right
		elif valLeft < threshold and valRight < threshold:
			key = keyboard.Key.up
		if not globalVars.KeyBufferCar.full():
			globalVars.KeyBufferCar.put(key)
			time.sleep(0.1)
	closePins()
	print("Auto drive thread stopped!")

def closePins():
	global sensorLeft, sensorRight
	if not sensorLeft.closed:
		sensorLeft.close()
	if not sensorRight.closed:
		sensorRight.close()

def initSensors():
	global sensorLeft, sensorRight
	sensorLeft = LineSensor(24)
	sensorRight = LineSensor(25)	
	
def exit_handler():
	print("Closing IR sensor pins")
	closePins()

def startAutoDriveThread():
	print("Auto drive thread starting....")
	initSensors()
	atexit.register(exit_handler)
	autoDriveThread = threading.Thread(target=autoDriveThreadFunc)
	autoDriveThread.start()
	return autoDriveThread
