
import sys
sys.path.append('../')
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat 
import config


''' This script is a unit test to test direction.  Directions are
forward, backward, turn left, turn right.  Turning is done by lowering
the speed of one side. For example, to turn left, the right wheels
need to spin slower than the left.
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
highSpeed = 200
lowSpeed = 50

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
	
def driveForward(driveTime = 1):
	for m in motors:
		m.setSpeed(highSpeed)
		m.run(amhat.FORWARD)	
	time.sleep(driveTime)
	
def driveBackward(driveTime = 1):
	for m in motors:
		m.setSpeed(highSpeed)
		m.run(amhat.BACKWARD)	
	time.sleep(driveTime)

def turnLeft(driveTime = 1):
	for lm in leftMotors:
		lm.setSpeed(lowSpeed)
		lm.run(amhat.FORWARD)
	for rm in rightMotors:
		rm.setSpeed(highSpeed)
		rm.run(amhat.FORWARD)
	time.sleep(driveTime)
	
def turnRight(driveTime = 1):
	for lm in leftMotors:
		lm.setSpeed(highSpeed)
		lm.run(amhat.FORWARD)
	for rm in rightMotors:
		rm.setSpeed(lowSpeed)
		rm.run(amhat.FORWARD)
	time.sleep(driveTime)


''' Drive Forward for 1 second'''
#driveForward(1)
#destroy()

''' Drive Backward for 1 second'''
#driveBackward(1)
#destroy()

''' Turn Left for 1 second '''
#turnLeft(1)
#destroy()

''' Turn Right for 1 second '''
#turnRight(1)
#destroy()

destroy()
