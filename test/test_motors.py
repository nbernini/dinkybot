
import sys
sys.path.append('../')
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat 
import config


''' This script is a basic test of each individual motor.  The script
will run the motor forward and backward as a basic unit test. You'll
need to set the motor number and the speed that the motor should run
at.  If the motors run in the opposite direction that the command, 
switch the positive/negative leads on the motor hat.
Motors are labeled:
1 - Left Front
2 - Left Rear
3 - Right Front
4 - Right Rear 
'''

# Set Motor Info
motorNumber = 4 
motorSpeed = 100


# Initialize Motor Hat 
motHAT = amhat(addr = config.motorHATaddress)

# Set motor number and speed
motor = motHAT.getMotor(motorNumber)
motor.setSpeed(motorSpeed)

# Forward
motor.run(amhat.FORWARD)
time.sleep(1)

# Backward
motor.run(amhat.BACKWARD)
time.sleep(1)

# Quit
motor.run(amhat.RELEASE)










