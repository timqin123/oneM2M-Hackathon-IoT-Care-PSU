import threading
from pynput import keyboard
import queue
import globalVars

def onPress(key):

	#print(f"\nPressed = {key}")
	try:
		key = key.char
	except AttributeError:
		pass

	if not globalVars.keyBufferMain.full() and key in ["1", "2"]:
		globalVars.keyBufferMain.put(key)
	if not globalVars.KeyBufferCar.full() and key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.down, keyboard.Key.space, keyboard.Key.left, keyboard.Key.right, "+", "-", "p"]:
		globalVars.KeyBufferCar.put(key)	
	if not globalVars.keyBufferServoA.full() and key in ["a", "d", "r", "p"]:
		globalVars.keyBufferServoA.put(key)
	if not globalVars.keyBufferServoB.full() and key in ["w", "s", "r", "p"]:
		globalVars.keyBufferServoB.put(key)
	if not globalVars.keyBufferServoC.full() and key in ["q", "e", "r", "p"]:
		globalVars.keyBufferServoC.put(key)
	if not globalVars.keyBufferServoD.full() and key in ["f", "g", "r", "p"]:
		globalVars.keyBufferServoD.put(key)
	
	if key == keyboard.Key.esc:
		globalVars.quitFlagMain = True
		globalVars.quitFlagCar = True
		globalVars.quitFlagArm = True
		globalVars.quitFlagAcme = True
		globalVars.quitFlagAutoDrive = True
		return False
		
def startKeyThread():
	print("Starting key thread")
	keyListenerThread = keyboard.Listener(on_press=onPress)
	keyListenerThread.start()
	return keyListenerThread
