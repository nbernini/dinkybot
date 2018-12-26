
''' 
    This file is the configuration values needed to initialize and run the
    robot, sensors, and camera.  
    
    The robot is a 4x4 vehicle equiped with 3 front facing Ultrasonic Rangefinder 
    sensors, 5 front mounted IR sensors, and a Camera.  Each of the 4 wheels is capable
    of independent motor speeds.  For this design, the Left and Right
    wheels will move in tandem (tank-like).  All sensors are are measured via an Arduino
    connected to the RaspberryPi(RPi) via serial connection.  The webcam is consumed
    by the RPi.
    
    There are multiple modes for this robot:
        1. Random Walk.  The robot will move forward until an object is found (using
            the Ultrasonic Sensors).  At that point, it will turn in a random direction
            and contiunue this process
        2. Line Follow.  The robot should follow a black line on a white surface (with the
            help of tuning parameters) using IR sensors.  This will use 2 different correction methods:
                a.) Basic correction (Rudementory "P" of "PID")
                b.) PID - will need to tune PID parameters
        3. Ball Following.  The robot should be able to follow a blue ball using a webcam as sensor input
        4. RC Car Mode.  The robot can be driven like a typcially RC car using different transmitters:
            a.) Keyboard inputs
            b.) WiiMote
        
    For consistency, lists of variables are ordered
    from left to right and front to back.  For drivetrain, lists are 
    ordered [Left Front, Left Back, Right Front, Right Back].
    
    Sensors are ordered left to right or front to back (where applicable)
    
    Where applicable, Left is negative, Right is positive direction
    
    Python Dependencies in requirements.txt
    
'''

""" Drive Train """
# Adafruit MotorHAT I2C Address
motorHATaddress=0x60

# Motor Names - all lists for motor information should be orded by this
motorNames=['LeftFront','LeftBack','RightFront','RightBack']

# Motors Positions for Adafruit_MotorHAT
motorPosLF=1
motorPosLB=2
motorPosRF=3
motorPosRB=4
motorPositions=[motorPosLF,motorPosLB,motorPosRF,motorPosRB]
motorsLeft=[motorPosLF,motorPosLB]
motorsRight=[motorPosRF,motorPosRB]

# Motor Multpliers - these are used to calibrate the motor speeds 
# as the motors used may have variance in speeds across a standard input.
# Default values of 1 apply no adjustment to the motors.  Values between
# (0,1) will slow the relative motor speed down.  Values (1,inf) will 
# increase the relative motor speed.
motorMultLF=1.0
motorMultLB=1.0
motorMultRF=1.0
motorMultRB=1.0
motorMultipliers=[motorMultLF,motorMultLB,motorMultRF,motorMultRB]
motorMultLeft=[motorMultLF,motorMultLB]
motorMultRight=[motorMultRF,motorMultRB]

# Motor Inital Speeds - Set these to zero to initialize, and then let the
# code determine the runtime speeds
motorSpeedLF=0
motorSpeedLB=0
motorSpeedRF=0
motorSpeedRB=0
motorSpeeds=[motorSpeedLF,motorSpeedLB,motorSpeedRF,motorSpeedRB]
motorSpeedsLeft=[motorSpeedLF,motorSpeedLB]
motorSpeedRight=[motorSpeedRF,motorSpeedLB]

# Speed Limits - Motors cannot function outside of these ranges [min, max]
speedLimits=[0,255]

# Default runtime speed
speedDefault=200 # Speeds range from 0 (no speed) to 255 (high speed)

# Default drive time (in seconds)
driveTime=0.01 # time to drive wheels before next drive command is initiated

# Turn Times (in seconds)
turnTimeRandom=1 # turn time in seconds for random walk


""" Serial Settings """
serialPort='/dev/ttyACM0'
serialBaudrate=9600
serialTimeout=1 # in seconds


""" IR Sensors """
irCalibrationCycles=4 # Number of cycles to run the calibration sweep.
irSweeptime=1000 # milliseconds to sweep calibration
irThreshold=50 # used as the +/- range around high values to signal if line is found (Needs tuned)
numIRSensors=5
irSensors=[0 for i in range(numIRSensors+1)] # place holder for sensor readings
irMins=[0 for i in range(numIRSensors+1)] # place holder for minimum values seen during calibration
irMaxs=[0 for i in range(numIRSensors+1)] # place holder for maximum values seen during calibration
irError=[2,1,0,-1,-2] # e.g. extreme error to left drives direction to right (positive)

""" Ultrasonic Sensors """
# Values for the ultrasonic rangefinder sensors are measured in cm
numUltraSensors=3
ultraDist=[0.0 for i in range(numUltraSensors+1)] # placeholder for inital values
ultraThesh=12.0 # if less than this value, consider an obstical is in the way
ultraCutoff=30.0 # if greater than this value, cap distance to this value.  Helps to control runaway values


""" Direction Corection Methods - Line Following """
# Basic - These get added/subtracted from the default speed to correct direction
corrections=[100,50,0,50,100]

# PID - These need tuned
lineTarget=0
lineKP=0.5
lineKI=0.5
lineKD=1
