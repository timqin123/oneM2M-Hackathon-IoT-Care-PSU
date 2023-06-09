import keyThread
import armThread
import globalVars
import carThread

globalVars.init()

globalVars.quitFlagArm = False

_keyThread = keyThread.startKeyThread()
carThreads = carThread.startCarThread()
armThreads = armThread.startArmThread()
_keyThread.join()
