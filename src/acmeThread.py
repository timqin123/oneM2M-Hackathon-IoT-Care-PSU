import threading
from pynput import keyboard
import queue
import globalVars
from acmeLib import init
import time
from acmeLib.config import *

keyMap = {"carForward" : keyboard.Key.up,\
	  "carBackward" : keyboard.Key.down,\
	  "carLeft" : keyboard.Key.left,\
	  "carRight" : keyboard.Key.right,\
	  "carAccelerate" : "+",\
          "carDecelerate" : "-",\
	  "carStop" : keyboard.Key.space,\
	  "carAutoDrive" : "p",\
	  "servoALeft" : "a",\
	  "servoARight" : "d",\
	  "servoBUp" : "w",\
	  "servoBDown" : "s",\
	  "servoCUp" : "e",\
	  "servoCDown" : "q",\
	  "servoDForward" : "f",\
	  "servoDBackward" : "g",\
	  "reset" : "r",\
	  "quit" : keyboard.Key.esc
	 }

def initAcme():

	print("Connecting to server....")
	connected = False
	while not connected:
		try:
			init.RETRIEVE (
			    to                      = cseBaseName,        
			    originator              = defaultOriginator, 
			    requestIdentifier       = '123',
			    releaseVersionIndicator = '3',
			)
			connected = True
			print("Connected!")
		except Exception:
			print("--> Probably Connection Refused")
			print("retrying....")
	
	print("Creating AE")
	init.CREATE (
	    to                      = cseBaseName,
	    originator              = aeOriginator,  # Assign an originator ID, must start with 'C'
	    requestIdentifier       = '123',                  
	    releaseVersionIndicator = '3',              
	    resourceType            = init.Type.AE,
	    primitiveContent = 
		{   
		    'm2m:ApplicationEntity': {
		        'resourceName':             'roboCar',  
		        'App-ID':                   'NroboCar',# Application ID, must start with 'N'
		        'requestReachability':      True,            
		        'supportedReleaseVersions': [ '3' ]  
		    }
		}
	)

	init.DELETE (
		to                      = cseBaseName + '/roboCar/Container', 
		originator              = aeOriginator,            
		requestIdentifier       = '123',                
		releaseVersionIndicator = '3',                  
	)

	print("Creating container")
	init.CREATE (
	    to                      = cseBaseName + '/roboCar', 
	    originator              = aeOriginator,       
	    requestIdentifier       = '123',               
	    releaseVersionIndicator = '3',                 
	    resourceType            = init.Type.Container, 
	    primitiveContent = 
		{
		    'm2m:Container': {
		        'resourceName': 'Container'
		    }
		},
	)

def acmeThreadFunc():
	while not globalVars.quitFlagAcme:
		content = None
		while not globalVars.quitFlagAcme and content is None:
			content = init.RETRIEVE (
				to                      = cseBaseName + '/roboCar/Container/la',
				originator              = aeOriginator,
				requestIdentifier       = '123',    
				releaseVersionIndicator = '3',   
				)
		print(f"Content1 = {content}")
		init.DELETE (
			to                      = cseBaseName + '/roboCar/Container/la', 
			originator              = aeOriginator,            
			requestIdentifier       = '123',                
			releaseVersionIndicator = '3',                  
		)

		print(f"Content2 = {content}")
		if content is not None and content in keyMap.keys():
			key = keyMap[content]
			if "car" in content or "quit" in content: 
				if not globalVars.KeyBufferCar.full():			
					globalVars.KeyBufferCar.put(key)
			elif "servoA" in content or "quit" in content or "reset" in content:
				if not globalVars.keyBufferServoA.full():
					globalVars.keyBufferServoA.put(key)
			elif "servoB" in content or "quit" in content or "reset" in content:
				if not globalVars.keyBufferServoB.full():
					globalVars.keyBufferServoB.put(key)
			elif "servoC" in content or "quit" in content or "reset" in content:
				if not globalVars.keyBufferServoC.full():
					globalVars.keyBufferServoC.put(key)
			elif "servoD" in content or "quit" in content or "reset" in content:
				if not globalVars.keyBufferServoD.full():
					globalVars.keyBufferServoD.put(key)

			if key == keyboard.Key.esc:
				globalVars.quitFlagAcme = True
		time.sleep(0.1)

def startAcmeThread():
	print("Initializing ACME server")
	initAcme()
	print("Starting ACME thread")
	acmeThread = threading.Thread(target=acmeThreadFunc, daemon=True)
	acmeThread.start()
	return acmeThread;
