import queue

def init():
	global quitFlagMain
	global quitFlagCar
	global quitFlagArm
	global quitFlagAcme
	global quitFlagAutoDrive
	global keyBufferMain
	global KeyBufferCar
	global keyBufferServoA
	global keyBufferServoB
	global keyBufferServoC
	global keyBufferServoD
	
	quitFlagMain = False
	quitFlagCar = False
	quitFlagArm = False
	quitFlagAcme = False
	quitFlagAutoDrive = True
	keyBufferMain = queue.Queue(5)
	KeyBufferCar = queue.Queue(5)
	keyBufferServoA = queue.Queue(5)
	keyBufferServoB = queue.Queue(5)
	keyBufferServoC = queue.Queue(5)
	keyBufferServoD = queue.Queue(5)
	
