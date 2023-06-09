from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep
import atexit
import queue
import threading
from pynput import keyboard
import time
import globalVars
import autoDriveThread

# up arrow
# down arrow
# left arrow
# right arrow
# +
# -
# spacebar - stop
# o
# p

INIT_MOTOR_SPEED = 35 #30
PWM_FREQ = 50
STEP = 5
SLEEP = 0.002

PWM_PIN_LEFT_MOT = 12
PWM_PIN_RIGHT_MOT = 13
IN1_PIN_LEFT_MOT = 5
IN2_PIN_LEFT_MOT = 6
IN1_PIN_RIGHT_MOT = 22
IN2_PIN_RIGHT_MOT = 23

pwm_pin_left_mot = None
pwm_pin_right_mot = None
cw_pin_left_mot = None
ccw_pin_left_mot = None
cw_pin_right_mot = None
ccw_pin_right_mot = None

leftMotorSpeed = 0
rightMotorSpeed = 0
leftMotorDirection = 0
rightMotorDirection = 0

leftMotorBuffer = queue.Queue(10)
rightMotorBuffer = queue.Queue(10)

def getCarStatus():
	if leftMotorSpeed != 0 and rightMotorSpeed != 0 and leftMotorDirection == 1 and rightMotorDirection == 1:
		return "movingForward"
	elif leftMotorSpeed != 0 and rightMotorSpeed != 0 and leftMotorDirection == -1 and rightMotorDirection == -1:
		return "movingBackward"
	elif leftMotorSpeed != 0 and rightMotorSpeed != 0 and leftMotorDirection == -1 and rightMotorDirection == 1:
		return "turningLeft"
	elif leftMotorSpeed != 0 and rightMotorSpeed != 0 and leftMotorDirection == 1 and rightMotorDirection == -1:
		return "turningRight"
	elif leftMotorSpeed == 0 and rightMotorSpeed == 0:
		return "stopped"
	else:
		print("Error status undefined")
	
def setForwardDirection(motor):
	global leftMotorDirection, rightMotorDirection
	if motor == "left":
		cw_pin_left_mot.value = 1
		ccw_pin_left_mot.value = 0
	elif motor == "right":
		cw_pin_right_mot.value = 1
		ccw_pin_right_mot.value = 0
	
def setBackwardDirection(motor):
	global leftMotorDirection, rightMotorDirection
	if motor == "left":
		cw_pin_left_mot.value = 0
		ccw_pin_left_mot.value = 1
	elif motor == "right":
		cw_pin_right_mot.value = 0
		ccw_pin_right_mot.value = 1		

def moveAtSpeed(motor, newSpeed):
	if motor == "left":
		if abs(leftMotorSpeed - newSpeed) > 20:
			sign = 1 if newSpeed > leftMotorSpeed else -1
			for i in range(leftMotorSpeed+sign, newSpeed+sign, sign*STEP):
				pwm_pin_left_mot.value = i/100.0
				time.sleep(SLEEP)
		else:
			pwm_pin_left_mot.value = newSpeed/100.0
		
	elif motor == "right":
		if abs(rightMotorSpeed - newSpeed) > 20:
			sign = 1 if newSpeed > rightMotorSpeed else -1
			for i in range(rightMotorSpeed+sign, newSpeed+sign, sign*STEP):
				pwm_pin_right_mot.value = i/100.0
				time.sleep(SLEEP)
		else:
			pwm_pin_right_mot.value = newSpeed/100.0


	print(leftMotorSpeed, rightMotorSpeed)

def StopMotor(motor):
	if motor == "left":
		if leftMotorSpeed > 20:
			prevSpeed = leftMotorSpeed
			for i in range(prevSpeed,0,-1*STEP):
				moveAtSpeed("left", i)
				time.sleep(SLEEP)
		cw_pin_left_mot.value = 0
		ccw_pin_left_mot.value = 0
		pwm_pin_left_mot.value = 0
	elif motor == "right":
		if rightMotorSpeed > 20:
			prevSpeed = rightMotorSpeed
			for i in range(prevSpeed,0,-1*STEP):
				moveAtSpeed("right", i)
				time.sleep(SLEEP)
		cw_pin_right_mot.value = 0
		ccw_pin_right_mot.value = 0
		pwm_pin_right_mot.value = 0
		
def leftMotorThreadFunc():
	print("Staring left motor thread")
	while not globalVars.quitFlagCar:
		if not leftMotorBuffer.empty():
			print(list(leftMotorBuffer.queue))
			instruction = leftMotorBuffer.get()
			if instruction == "stop":
				StopMotor("left")
			elif instruction in ["start", "accelerate", "decelerate"]:
				moveAtSpeed("left", leftMotorSpeed)
			elif instruction == "forwardDirection":
				setForwardDirection("left")
			elif instruction == "backwardDirection":
				setBackwardDirection("left")
		time.sleep(0.01)
	print("Left motor thread stopped")

def rightMotorThreadFunc():
	while not globalVars.quitFlagCar:
		if not rightMotorBuffer.empty():
			print(list(rightMotorBuffer.queue))
			instruction = rightMotorBuffer.get()
			if instruction == "stop":
				StopMotor("right")
			elif instruction in ["start", "accelerate", "decelerate"]:
				moveAtSpeed("right", rightMotorSpeed)
			elif instruction == "forwardDirection":
				setForwardDirection("right")
			elif instruction == "backwardDirection":
				setBackwardDirection("right")
		time.sleep(0.01)
	print("Right motor thread stopped")

def controlThreadFunc():
	print("Starting car control thread")
	global leftMotorSpeed, rightMotorSpeed, leftMotorDirection, rightMotorDirection
	prevLeftMotorSpeed = prevRightMotorSpeed = 0
	_autoDriveThread = None
	while not globalVars.quitFlagCar:
		if not globalVars.KeyBufferCar.empty():
			print(list(globalVars.KeyBufferCar.queue))
			key = globalVars.KeyBufferCar.get()
			print(f"--> {key}")
			carStatus = getCarStatus()
			if key == keyboard.Key.space:
				globalVars.KeyBufferCar.queue.clear()
				if _autoDriveThread is not None:
					globalVars.quitFlagAutoDrive = True
					print("Waitig auto drive thread to stop")
					_autoDriveThread.join()
					_autoDriveThread = None
				leftMotorBuffer.put("stop")
				rightMotorBuffer.put("stop")
				leftMotorSpeed = 0
				rightMotorSpeed = 0
				leftMotorDirection = 0
				rightMotorDirection = 0
			elif key == keyboard.Key.up:
				if carStatus == "stopped":
					leftMotorSpeed = INIT_MOTOR_SPEED
					rightMotorSpeed = INIT_MOTOR_SPEED
					leftMotorBuffer.put("forwardDirection")
					rightMotorBuffer.put("forwardDirection")
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				elif carStatus == "movingBackward":
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					leftMotorBuffer.put("forwardDirection")
					rightMotorBuffer.put("forwardDirection")
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				elif carStatus == "turningLeft" or carStatus == "turningRight":
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					leftMotorBuffer.put("forwardDirection")
					rightMotorBuffer.put("forwardDirection")
					leftMotorSpeed = rightMotorSpeed = INIT_MOTOR_SPEED
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				leftMotorDirection = 1
				rightMotorDirection = 1
			elif key == keyboard.Key.down:
				if carStatus == "stopped":
					leftMotorSpeed = INIT_MOTOR_SPEED
					rightMotorSpeed = INIT_MOTOR_SPEED
					leftMotorBuffer.put("backwardDirection")
					rightMotorBuffer.put("backwardDirection")
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				elif carStatus == "movingForward":
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					leftMotorBuffer.put("backwardDirection")
					rightMotorBuffer.put("backwardDirection")
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				elif carStatus == "turningLeft" or carStatus == "turningRight":
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					leftMotorBuffer.put("backwardDirection")
					rightMotorBuffer.put("backwardDirection")
					leftMotorSpeed = rightMotorSpeed = INIT_MOTOR_SPEED
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
				leftMotorDirection = -1
				rightMotorDirection = -1
			elif key == keyboard.Key.left:
				if carStatus != "turningLeft":
					prevLeftMotorSpeed = leftMotorSpeed
					prevRightMotorSpeed = rightMotorSpeed
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					time.sleep(0.1)
					leftMotorBuffer.put("backwardDirection")
					rightMotorBuffer.put("forwardDirection")
					leftMotorSpeed = 99
					rightMotorSpeed = 99
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")	
					time.sleep(0.1)
					leftMotorDirection = -1
					rightMotorDirection = 1
					#leftMotorSpeed = prevLeftMotorSpeed
					#rightMotorSpeed = prevRightMotorSpeed
			elif key == keyboard.Key.right:
				if carStatus != "turningRight":
					prevLeftMotorSpeed = leftMotorSpeed
					prevRightMotorSpeed = rightMotorSpeed
					leftMotorBuffer.put("stop")
					rightMotorBuffer.put("stop")
					time.sleep(0.1)
					leftMotorBuffer.put("forwardDirection")
					rightMotorBuffer.put("backwardDirection")
					leftMotorSpeed = 99
					rightMotorSpeed = 99
					leftMotorBuffer.put("start")
					rightMotorBuffer.put("start")
					time.sleep(0.1)
					leftMotorDirection = 1
					rightMotorDirection = -1
					#leftMotorSpeed = prevLeftMotorSpeed
					#rightMotorSpeed = prevRightMotorSpeed
			elif key == "+":
				if carStatus != "stopped":
					leftMotorSpeed += STEP
					rightMotorSpeed += STEP 
					if leftMotorSpeed > 100:
						print(f"Left motor Max speed reached = {leftMotorSpeed}")
						leftMotorSpeed = 99
					if rightMotorSpeed > 100:
						print(f"Right motor Max speed reached = {rightMotorSpeed}")
						rightMotorSpeed = 99
					leftMotorBuffer.put("accelerate")	
					rightMotorBuffer.put("accelerate")
			elif key == "-":
				if carStatus in ["movingForward", "movingBackward"]:
					leftMotorSpeed -= STEP
					rightMotorSpeed -= STEP 
					if leftMotorSpeed < 0:
						print(f"Left motor Min speed reached = {leftMotorSpeed}")
						leftMotorSpeed = 0
					if rightMotorSpeed < 0:
						print(f"Right motor Min speed reached = {rightMotorSpeed}")
						rightMotorSpeed = 0
					leftMotorBuffer.put("decelerate")	
					rightMotorBuffer.put("decelerate")
			elif key == "p":
				leftMotorBuffer.put("stop")
				rightMotorBuffer.put("stop")
				leftMotorSpeed = INIT_MOTOR_SPEED
				rightMotorSpeed = INIT_MOTOR_SPEED
				leftMotorDirection = 1
				rightMotorDirection = 1
				leftMotorBuffer.put("forwardDirection")
				rightMotorBuffer.put("forwardDirection")
				leftMotorBuffer.put("start")
				rightMotorBuffer.put("start")
			
				if _autoDriveThread is None:
					globalVars.quitFlagAutoDrive = False
					_autoDriveThread = autoDriveThread.startAutoDriveThread()
		time.sleep(0.01)
	closePins()
	print("Car control thread stopped")

def closePins():
	global pwm_pin_left_mot, pwm_pin_right_mot, cw_pin_left_mot, ccw_pin_left_mot, cw_pin_right_mot, ccw_pin_right_mot
	if pwm_pin_left_mot.closed:
		pwm_pin_left_mot.close()
	if pwm_pin_right_mot.closed:
		pwm_pin_right_mot.close()
	if cw_pin_left_mot.closed:
		cw_pin_left_mot.close()
	if ccw_pin_left_mot.closed:
		ccw_pin_left_mot.close()
	if cw_pin_right_mot.closed:
		cw_pin_right_mot.close()
	if ccw_pin_right_mot.closed:
		ccw_pin_right_mot.close()

# Exit handerler - Turn off all servos before ending!
def exit_handler():
	print("My application is ending!")
	print("Setting all car motor PWM to 0")
	StopMotor("left")
	StopMotor("right")
	closePins()

def initCar():
	global pwm_pin_left_mot, pwm_pin_right_mot, cw_pin_left_mot, ccw_pin_left_mot, cw_pin_right_mot, ccw_pin_right_mot
	print("Initializing car")
	pwm_pin_left_mot = PWMOutputDevice (PWM_PIN_LEFT_MOT,True, 0, PWM_FREQ)
	pwm_pin_right_mot = PWMOutputDevice (PWM_PIN_RIGHT_MOT,True, 0, PWM_FREQ)
	cw_pin_left_mot = DigitalOutputDevice (IN1_PIN_LEFT_MOT, True, 0)
	ccw_pin_left_mot = DigitalOutputDevice (IN2_PIN_LEFT_MOT, True, 0)
	cw_pin_right_mot = DigitalOutputDevice (IN1_PIN_RIGHT_MOT, True, 0)
	ccw_pin_right_mot = DigitalOutputDevice (IN2_PIN_RIGHT_MOT, True, 0)

def startCarThread():
	
	initCar()
	atexit.register(exit_handler)
	controlThread = threading.Thread(target=controlThreadFunc)
	leftMotorThread = threading.Thread(target=leftMotorThreadFunc)
	rightMotorThread = threading.Thread(target=rightMotorThreadFunc)
	controlThread.start()
	leftMotorThread.start()
	rightMotorThread.start()
	return [controlThread, leftMotorThread, rightMotorThread]
	

#if __name__ == "__main__":
	#while True:
	#globalVars.init()
	#_carThread = startCarThread()
	#_keyThread = keyThread.startKeyThread()	
	#_acmeThread = acmeThread.startAcmeThread()

	#_keyThread.join()
	#_acmeThread.join()
	#_carThread.join()
          
	
