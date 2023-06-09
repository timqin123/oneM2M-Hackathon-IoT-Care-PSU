from gpiozero import LineSensor
from signal import pause
from gpiozero.tools import booleanized

sensor1 = LineSensor(24)
sensor2 = LineSensor(25)

"""
sensor1.when_line = lambda: print('left Line detected')
#sensor1.when_no_line = lambda: print('left No line detected')

sensor2.when_line = lambda: print('Right Line detected')
#sensor2.when_no_line = lambda: print('No line detected')
pause()
"""

#bs1 = booleanized(sensor1, 0.5, 1)
#bs2 = booleanized(sensor2, 0.5, 1)

while True:
	print(f"Left = {sensor1.value}    Right = {sensor2.value}")
