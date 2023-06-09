import time
import Adafruit_PCA9685
import atexit
from pynput import keyboard
import threading
import globalVars

pwm = None 

INIT_PWM_LEVEL = 300
# ports
portA = 2
portB = 5
portC = 8
portD = 15

# A = a,d
# B = w,s
# c = q,e
# D = f,g

# PWM min
pwmMinA = 200
pwmMinB = 200
pwmMinC = 200
pwmMinD = 100

# PWM max
pwmMaxA = 400
pwmMaxB = 400
pwmMaxC = 400
pwmMaxD = 500

# PWM step
stepA = 50
stepB = 20
stepC = 20
stepD = 50

def servoThreadFuncA():
	global pwm
	
	pwmLevel = INIT_PWM_LEVEL
	while not globalVars.quitFlagArm:
		if not globalVars.keyBufferServoA.empty():
			key = globalVars.keyBufferServoA.get()
			if key == "a":
				#print("Servo Thread A = a pressed")
				if pwmLevel >= pwmMaxA:
					print("Max PWM Level reached")
				else:
					if (pwmLevel + stepA) > pwmMaxA:
						pwmLevel = pwmMaxA
					else:
						pwmLevel += stepA
					pwm.set_pwm(portA, 0, pwmLevel)
				print(f"PWM A = {pwmLevel}")
			elif key == "d":
				#print("Servo Thread A = d pressed")
				if pwmLevel <= pwmMinA:
					print("Min PWM Level reached")
				else:
					if (pwmLevel - stepA) < pwmMinA:
						pwmLevel = pwmMinA
					else:
						pwmLevel -= stepA
					pwm.set_pwm(portA, 0, pwmLevel)
				print(f"PWM A = {pwmLevel}")
			elif key == "r":
				print("Ressetting servo A")
				pwmLevel = INIT_PWM_LEVEL
				pwm.set_pwm(portA, 0, pwmLevel)
				print(f"PWM A = {pwmLevel}")
			elif key == "p":
				print(f"PWM A = {pwmLevel}")
			
		time.sleep(0.1)
		pwm.set_pwm(portA, 0, 0)
	print("A stopped")

def servoThreadFuncB():
	global pwm
	
	pwmLevel = INIT_PWM_LEVEL
	while not globalVars.quitFlagArm:
		if not globalVars.keyBufferServoB.empty():
			print(list(globalVars.keyBufferServoB.queue))
			key = globalVars.keyBufferServoB.get()
			if key == "w":
				#print("Servo Thread B = w pressed")
				if pwmLevel >= pwmMaxB:
					print("Max PWM Level reached")
				else:
					if (pwmLevel + stepB) > pwmMaxB:
						pwmLevel = pwmMaxB
					else:
						pwmLevel += stepB
					pwm.set_pwm(portB, 0, pwmLevel)
				print(f"PWM B = {pwmLevel}")
			elif key == "s":
				#print("Servo Thread B = s pressed")
				if pwmLevel <= pwmMinB:
					print("Min PWM Level reached")
				else:
					if (pwmLevel - stepB) < pwmMinB:
						pwmLevel = pwmMinB
					else:
						pwmLevel -= stepB
					pwm.set_pwm(portB, 0, pwmLevel)
				print(f"PWM B = {pwmLevel}")
			elif key == "r":
				print("Ressetting servo B")
				pwmLevel = INIT_PWM_LEVEL
				pwm.set_pwm(portB, 0, pwmLevel)
				print(f"PWM B = {pwmLevel}")
			elif key == "p":
				print(f"PWM B = {pwmLevel}")
				
		time.sleep(0.1)
		pwm.set_pwm(portB, 0, 0)
	print("B stopped")

def servoThreadFuncC():
	global pwm

	pwmLevel = INIT_PWM_LEVEL
	while not globalVars.quitFlagArm:
		if not globalVars.keyBufferServoC.empty():
			print(list(globalVars.keyBufferServoC.queue))
			key = globalVars.keyBufferServoC.get()
			if key == "q":
				#print("Servo Thread C = q pressed")
				if pwmLevel >= pwmMaxC:
					print("Max PWM Level reached")
				else:
					if (pwmLevel + stepC) > pwmMaxC:
						pwmLevel = pwmMaxC
					else:
						pwmLevel += stepC
					pwm.set_pwm(portC, 0, pwmLevel)
				print(f"PWM C = {pwmLevel}")
			elif key == "e":
				#print("Servo Thread C = e pressed")
				if pwmLevel <= pwmMinC:
					print("Min PWM Level reached")
				else:
					if (pwmLevel - stepC) < pwmMinC:
						pwmLevel = pwmMinC
					else:
						pwmLevel -= stepC
					pwm.set_pwm(portC, 0, pwmLevel)
				print(f"PWM C = {pwmLevel}")
			elif key == "r":
				print("Ressetting servo C")
				pwmLevel = INIT_PWM_LEVEL
				pwm.set_pwm(portC, 0, pwmLevel)
				print(f"PWM C = {pwmLevel}")
			elif key == "p":
				print(f"PWM C = {pwmLevel}")
				
		time.sleep(0.1)
		pwm.set_pwm(portC, 0, 0)
	print("C stopped")

def servoThreadFuncD():
	global pwm

	pwmLevel = INIT_PWM_LEVEL
	while not globalVars.quitFlagArm:
		if not globalVars.keyBufferServoD.empty():
			print(list(globalVars.keyBufferServoD.queue))
			key = globalVars.keyBufferServoD.get()
			if key == "f":
				#print("Servo Thread D = f pressed")
				if pwmLevel >= pwmMaxD:
					print("Max PWM Level reached")
				else:
					if (pwmLevel + stepD) > pwmMaxD:
						pwmLevel = pwmMaxD
					else:
						pwmLevel += stepD
					pwm.set_pwm(portD, 0, pwmLevel)
				print(f"PWM D = {pwmLevel}")
			elif key == "g":
				#print("Servo Thread D = g pressed")
				if pwmLevel <= pwmMinD:
					print("Min PWM Level reached")
				else:
					if (pwmLevel - stepD) < pwmMinD:
						pwmLevel = pwmMinD
					else:
						pwmLevel -= stepD
					pwm.set_pwm(portD, 0, pwmLevel)
				print(f"PWM D = {pwmLevel}")
			elif key == "r":
				print("Ressetting servo D")
				pwmLevel = INIT_PWM_LEVEL
				pwm.set_pwm(portD, 0, pwmLevel)
				print(f"PWM D = {pwmLevel}")
			elif key == "p":
				print(f"PWM D = {pwmLevel}")
				
		time.sleep(0.1)
		pwm.set_pwm(portD, 0, 0)
	print("D stopped")

def exit_handler():
    global pwm
    print("My application is ending!")
    print("Setting all servo PWM to 0")
    pwm.set_all_pwm(0, 0)

def initServos():
	global pwm
	print(f"Servo ports = {[portA, portB, portC, portD]}")

	print("Initializing PWM ports....")
	pwm = Adafruit_PCA9685.PCA9685()
	pwm.set_pwm_freq(50)

	atexit.register(exit_handler) 

	pwm.set_all_pwm(0, INIT_PWM_LEVEL)
	time.sleep(0.1)
	print("sleeping")
	pwm.set_all_pwm(0, 0)
	time.sleep(0.1)
	print("PWM ports initialized")

def startArmThread():
	initServos()
	servoThreadA = threading.Thread(target=servoThreadFuncA)
	servoThreadB = threading.Thread(target=servoThreadFuncB)
	servoThreadC = threading.Thread(target=servoThreadFuncC)
	servoThreadD = threading.Thread(target=servoThreadFuncD)
	servoThreadA.start()
	servoThreadB.start()
	servoThreadC.start()
	servoThreadD.start()
	return [servoThreadA, servoThreadB, servoThreadC, servoThreadD]
