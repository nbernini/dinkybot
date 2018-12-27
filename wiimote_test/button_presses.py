
import sys
sys.path.append('../')

import time
from pprint import pprint
from WiiMoteWrapper import WiiMoteWrapper

# Initialize Wiimote
wm = WiiMoteWrapper()

# Get list of buttons
button_list = wm.get_button_list()
print button_list

# Connect
wm.connect(rumble = True)


# Loop for 20 seconds
start = time.time()
duration = time.time() - start
while duration < 20:

	# Check if 'a' button is pressed
	#print 'Button A is pressed: {}'.format(wm.check_button('a'))
	
	# Check if 'a' and 'b' are pressed together
	#print 'Buttons A and B are pressed: {}'.format(wm.check_button(['a','b']))

	# Check if '+' and '-' are pressed together, disconnect and quit
	print 'waiting ...'
	if wm.check_button(['+','-']):
		wm.disconnect(rumble = True)
		quit()
		
	time.sleep(0.1)
	duration = time.time() - start

