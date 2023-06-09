import acmeThread
import carThread
import keyThread
import armThread
import globalVars
import time

carThreads = None
armThreads = None

globalVars.init()

_acmeThread = acmeThread.startAcmeThread()
_keyThread = keyThread.startKeyThread()
carThreads = carThread.startCarThread()
armThreads = armThread.startArmThread()

