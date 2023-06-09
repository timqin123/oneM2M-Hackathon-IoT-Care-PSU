from pynput import keyboard
from acmeLib import init
from acmeLib.config import *

def push2AcmeServer(content): 
	try:
		"""
		init.DELETE (
		    to                      = cseBaseName + '/roboCar/Container/la', 
		    originator              = aeOriginator,         
		    requestIdentifier       = '123',              
		    releaseVersionIndicator = '3',                 
		)
		"""

		init.CREATE (
		    to                      = cseBaseName + '/roboCar/Container', 
		    originator              = aeOriginator, 
		    requestIdentifier       = '123', 
		    releaseVersionIndicator = '3',
		    resourceType            = init.Type.ContentInstance,
		    primitiveContent = 
			{
			    'm2m:ContentInstance': {
				'contentInfo': 'text/plain:0',              
				'content': content              
			    }
			}
		)
	except Exception:
		print("Error while writing to ACME server")


def onPress(key):
	#print(f"\nPressed = {key}")
	try:
		key = key.char
	except AttributeError:
		pass

	if key == keyboard.Key.up:
		push2AcmeServer("carForward")
	elif key == keyboard.Key.down:	
		push2AcmeServer("carBackward")
	elif key == keyboard.Key.left:	
		push2AcmeServer("carLeft")
	elif key == keyboard.Key.right:	
		push2AcmeServer("carRight")
	elif key == "+":	
		push2AcmeServer("carAccelerate")
	elif key == "-":	
		push2AcmeServer("carDecelerate")
	elif key == keyboard.Key.space:	
		push2AcmeServer("carStop")
	elif key == "a":
		push2AcmeServer("servoALeft")
	elif key == "d":
		push2AcmeServer("servoARight")
	elif key == "w":
		push2AcmeServer("servoBUp")
	elif key == "s":
		push2AcmeServer("servoBDown")
	elif key == "e":
		push2AcmeServer("servoCUp")
	elif key == "q":
		push2AcmeServer("servoCDown")
	elif key == "f":
		push2AcmeServer("servoDForward")
	elif key == "g":
		push2AcmeServer("servoDBackward")
	elif key == "r":
		push2AcmeServer("reset")
	elif key == keyboard.Key.esc:
		push2AcmeServer("quit")
	else:
		push2AcmeServer(key)

	if key == keyboard.Key.esc:
		return False

keyListenerThread = keyboard.Listener(on_press=onPress)
keyListenerThread.start()
keyListenerThread.join()

