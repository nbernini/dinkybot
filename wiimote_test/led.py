
import sys
sys.path.append('../')

import time
from pprint import pprint
from WiiMoteWrapper import WiiMoteWrapper

# Initialize Wiimote
wm = WiiMoteWrapper()

# Connect
wm.connect(rumble = True)

''' List represents each LED on/off status '''
states = [
	[0,0,0,0],
	[1,0,0,0],
	[0,1,0,0],
	[0,0,1,0],
	[0,0,0,1],
	[0,1,1,0],
	[1,0,0,1],
	[1,1,1,1],
	[1,0,1,1]
]

for s in states:
	wm.led(s)
	time.sleep(1)


