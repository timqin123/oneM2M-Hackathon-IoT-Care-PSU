import acmeThread
import globalVars
import time


globalVars.init()

_acmeThread = acmeThread.startAcmeThread()
_acmeThread.join()
