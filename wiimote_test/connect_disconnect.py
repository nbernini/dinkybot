
import sys
sys.path.append('../')

import time
from pprint import pprint
from WiiMoteWrapper import WiiMoteWrapper

# Initialize Wiimote
wm = WiiMoteWrapper()

# Connect
wm.connect(rumble = True)

# Wait 3 seconds
time.sleep(3)

# Disconnect
wm.disconnect(rumble = True)
