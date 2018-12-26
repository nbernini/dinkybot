
import sys
sys.path.append('../')
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat 
import cwiid
import config



''' This script is a basic usage of using the Nintendo WiiMote to 
drive the robot. Once the remote is connected, the D-pad will drive
the robot.  Hitting plus and minus togther should quit the program.
Directions:
Up - Forward
Down - Backward
Left - Turn Left
Right - Turn Right

Motors are labeled:
1 - Left Front
2 - Left Rear
3 - Right Front
4 - Right Rear 
'''

# Set Motor Info
motorNames = config.motorNames
print 'Motor Names: {}'.format(motorNames)
motorNumbers = config.motorPositions
print 'Motor Numbers: {}'.format(motorNumbers)
leftMotorNumbers = [1,2]
rightMotorNumbers = [3,4]

# Set Speeds
highSpeed = 500
lowSpeed = 50

# Drive Time (in seconds)
driveTime=0.01

# Initialize Motor Hat 
motHAT = amhat(addr = config.motorHATaddress)

# Setup motors
motors = [motHAT.getMotor(m) for m in motorNumbers]
leftMotors = [motHAT.getMotor(lm) for lm in leftMotorNumbers]
rightMotors = [motHAT.getMotor(rm) for rm in rightMotorNumbers]

def destroy():
	# Kill all motor action
	for m in motors:
		m.run(amhat.RELEASE)
	
def driveForward(driveTime = driveTime):
	for m in motors:
		m.setSpeed(highSpeed)
		m.run(amhat.FORWARD)	
	time.sleep(driveTime)
	destroy()
	
def driveBackward(driveTime = driveTime):
	for m in motors:
		m.setSpeed(highSpeed)
		m.run(amhat.BACKWARD)	
	time.sleep(driveTime)
	destroy()

def turnLeft(driveTime = driveTime):
	for lm in leftMotors:
		lm.setSpeed(highSpeed)
		lm.run(amhat.BACKWARD)
	for rm in rightMotors:
		rm.setSpeed(highSpeed)
		rm.run(amhat.FORWARD)
	time.sleep(driveTime)
	destroy()
	
def turnRight(driveTime = driveTime):
	for lm in leftMotors:
		lm.setSpeed(highSpeed)
		lm.run(amhat.FORWARD)
	for rm in rightMotors:
		rm.setSpeed(highSpeed)
		rm.run(amhat.BACKWARD)
	time.sleep(driveTime)
	destroy()

''' Main Program '''
# This code attempts to connect to your Wiimote and if it fails the program quits
button_delay = 0.1
print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)
try:
  wii = cwiid.Wiimote()
  print 'Connected.  Use the D-Pad to drive the robot.'
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()
time.sleep(3)
wii.rpt_mode = cwiid.RPT_BTN  
  
check = True
while check:
	# Checks if any buttons are pressed
	buttons = wii.state['buttons']
	
	# Detects whether + and - are held down and if they are it quits the program
	if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
		print '\nClosing connection ...'
		# NOTE: This is how you RUMBLE the Wiimote
		wii.rumble = 1
		time.sleep(1)
		wii.rumble = 0
		#exit(wii)	
		check = False
		destroy()
	
	# Check Direction
	if (buttons & cwiid.BTN_DOWN):
		driveBackward(driveTime = driveTime)
	if (buttons & cwiid.BTN_UP):
		driveForward(driveTime = driveTime)
	if (buttons & cwiid.BTN_LEFT):
		turnLeft(driveTime = driveTime)
	if (buttons & cwiid.BTN_RIGHT):
		turnRight(driveTime = driveTime)

# Kill motors
destroy()

 
