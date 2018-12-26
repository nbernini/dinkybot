""" Main Robot Class """

import random
import serial
import config
import time
import operator
from adafruit_motor_hat.MotorHat import AdafruitMotorHAT as amhat 
from adafruit_motor_hat.MotorHat import AdafruitDCMotor as adamo

class Robot(object):
    
    def __init__(self):
        self.ser = serial.Serial(port=config.serialPort, baudrate=config.serialBaudrate, timeout=config.serialTimeout)
        self.drivetrain = DriveTrain()
        self.ultra_sensors = UltrasonicSensor(self.ser)
        self.ir_sensors = IRSensor(self.ser)
        # self.camera = TODO
        # self.upload_arduino = TODO

    def random_walk(self):
        ''' Randomly move until an object is seen.  This method should be put in a while loop in the 
            main script.  If object is on left, turn right.  If object is on right, 
            turn left.  If object is straight ahead, turn to side with most room.  If both left and right have
            equal distance to object, turn in a random direction and repeat
        '''
        # initialize speed and drivetime
        speed = self.drivetrain.defaultSpeed
        driveTime = self.drivetrain.driveTime
        
        # check distances. value of 1 means object has been reached
        # returns [left, mid, right]
        dist = self.ultra_sensors.check_distances()
        
        # Check if object on sides
        if dist[0]: # Object on left, turn right
            leftSpeed = speed
            rightspeed = -speed
        elif dist[-1]: # Object on right, turn left
            leftSpeed = -speed
            rightSpeed = speed
        else: # Else, drive forward
            leftSpeed = speed
            rightSpeed = speed
            
        # Check if object straight ahead
        if dist[1]:
            # get readings
            readings = self.ultra_sensors.get_readings()
            
            # stop 
            self.drivetrain.drive(leftSpeed = 0, rightSpeed = 0)
            
            # wait
            time.sleep(1)
            
            # backup
            self.drivetrain.drive(leftSpeed = -speed, rightSpeed = -speed, driveTime = 1)
            
            # preferred direction - if left>right turn left, if right>left turn left, else turn random
            perf_dir = readings[0] - readings[1]
            if perf_dir == 0: # turn random
                perf_dir = random.choice([-1,1])
            if perf_dir < 0: # turn right
                leftSpeed = speed
                rightSpeed = -speed
            elif perf_dir > 0: # turn left
                leftSpeed = -speed
                rightSpeed = speed
            
            # Turn Time
            driveTime = config.turnTimeRandom
            
        # drive
        self.drivetrain.drive(leftSpeed = leftSpeed, rightSpeed = rightSpeed, driveTime = driveTime)
    
    def folow_line(self, mode = 'basic'):
        ''' Follow a black line on a while surface.  This method should be put inside a while loop in the 
            main script and should have the calibrate method called (outside the loop) prior to running this 
            method.  There are two different modes to apply corrective action.  'basic' applies a rudementary
            correction method based off of proportional directional error.  'pid' applies a full PID correction,
            where parameters are tunable.
        '''
        # initialize
        speed = self.drivetrain.defaultSpeed
        driveTime = self.drivetrain.driveTime
        pid = PID(target = config.lineTarget, kp = config.lineKP, ki = config.lineKI, kd = config.lineKD)        
        
        # calc correction
        corr = self.ir_sensors.calculate_correction(mode = mode, pid=pid)
        
        # apply correction
        leftSpeed = corr[0](speed,corr[1])
        rightSpeed = corr[0](speed,corr[2])
        
        # drive
        self.drivetrain.drive(leftSpeed = leftSpeed, rightSpeed = rightSpeed, driveTime = driveTime)
        
    def follow_ball(self):
        ''' '''
        # pid = PID(target = 0, kp = config.ballKP, ki = config.ballKI, kd = config.ballKD)        
        
    def calibrate_line(self):
        ''' Calibrate the min/max values seen by the IR sensors by sweeping back and forth across the line
            and recording min/max values read by the analog input of the IR sensor
        '''
        # set up cycle count loop 
        direction = 1 
        cycle = 0 

        # sweep loop        
        while cycle < config.irCalibrationCycles + 1: 
            millisOld = int(round(time.time()*1000)) 
            millisNew = millisOld
    
            #For the duration of sweepTime, drive the motors and read the IR sensors. 
            while((millisNew-millisOld)<sweepTime):
                # initialize speeds
                leftSpeed = self.drivetrain.defaultSpeed * direction 
                rightSpeed = self.drivetrain.defaultSpeed * -direction 
                
                # drive the motors 
                drivetrain.drive(leftSpeed = leftSpeed, rightSpeed = rightSpeed)
                
                # read sensors 
                readings = self.ir_sensors.get_readings()
                
                # update IR limits
                self.ir_sensors.update_limits(readings)
    
                # reset time counter
                millisNew = int(round(time.time()*1000)) 
                
            # reverse direction 
            direction = -direction 
            
            # increment cycles 
            cycle += 1 
            
        # When the cycles have completed, drive the robot forward. 
        # drive forward 
        self.drivetrain.drive()
        
    def destroy(self):
        self.drivetrain.destroy()
        # self.ultra_sensors.destroy()
        # self.ir_sensors.destroy()
        
class DriveTrain(object):
    """ Object for controlling drive train """
    def __init__(self):
        self.motHAT = amhat(addr=config.motorHATaddress) 
        self.motors = {
            'left': {
                'motors': [self.motHAT.getMotors(i) for i in config.motorsLeft], # get motors from config file positions
                'speed': [config.speedDefault for i in config.motorsLeft], # set speed for each motor to default
                'multiplier': config.motorMultLeft
            },
            'right': {
                'motors': [self.motHAT.getMotors(i) for i in config.motorsRight],
                'speed': [config.speedDefault for i in config.motorsRight],
                'multiplier': config.motorMultRight
            }
        }
        self.defaultSpeed = config.speedDefault
        self.driveTime = config.driveTime
        self.speedLimits = config.speedLimits # list [min,max]
        
    def set_speed(self, leftSpeed = config.speedDefault, rightSpeed = config.speedDefault):
        """ 
            Updates self.motors speed keypair and sets motorhat speed.  Note, speed can be negative based on 
            direction, so we force the absolute value.  Also, must take the integer value for MotorHAT requirements
        """
        
        # Loop through drive train sides
        for side, speed in zip(['left', 'right'],[leftSpeed, rightSpeed]):
            # Update Speed Value
            self.motors[side]['speed'] = [self._check_speed(speed * m) for m in self.motors[side]['multipliers']] # applying multiplier
            
            # Loop through motors w/in a side
            for motor, speed in zip(self.motors[side]['motors'], self.motors[side]['speed']):
                # Set MotorHAT Speed
                motor.setSpeed(int(abs(speed))) # force integer and take absolute value 

    def drive(self, leftSpeed = config.speedDefault, rightSpeed = config.speedDefault, driveTime = config.driveTime):
        ''' Drives Motors'''
        
        #  Set Speed
        self.set_speed(leftSpeed, rightSpeed)
        
        # Run the Motors.  Positive values drive forward.  Negative values drive backwards
        # Left Channel
        if leftSpeed < 0:
            for m in motors['left']['motors']:
                m.run(amhat.BACKWARD)
        else:
            for m in motors['left']['motors']:
                m.run(amhat.FORWARD)
        
        # Right Channel
        if rightSpeed < 0:
            for m in motors['right']['motors']:
                m.run(amhat.BACKWARD)
        else:
            for m in motors['right']['motors']:
                m.run(amhat.FORWARD)
        
        # Delay
        time.sleep(driveTime)
    
    def destroy(self):
        ''' Releases Motors '''
        for m in self.motors['left']['motors']+self.motors['right']['motors']:
            m.run(amhat.RELEASE)

    def _check_speed(self, speed):
        ''' Checks that speed is between motor's absolute min/max values.  Returns min/max if
            speed violates these
        '''
        check = max(min(speed,self.speedLimits[1]),self.speedLimits[0])
        
class SerialWrapper(object):
    ''' Wrapper for Serial communication between RPi and Adurino '''
    def __init__(self):
        self.port = config.serialPort
        self.baudrate = config.serialBaudrate
        self.timeout = config.serialTimeout
        self.ser = serial.Serial(port=config.serialPort, baudrate=config.serialBaudrate, timeout=config.serialTimeout)
        
    def read(self, delimiter = ','):
        ''' Returns a parsed list of values. '''
        # read the serial port 
        val = self.ser.readline().decode('utf-8') 
    
        # parse the serial string 
        parsed = [x.rstrip() for x in val.split(delimiter)]
        
        # flush the serial buffer of any extra bytes 
        ser.flushInput()

        return parsed

    def write(self,data):
        ''' TODO '''
        
class UltrasonicSensor(object):
    
    def __init__(self, ser):
        self.ser=ser # serial wrapper
        self.num_sensors = config.numUltraSensors
        self.distances = config.ultraDist
        self.cutoff = config.ultraCutoff
        self.thresh = config.irThreshold
        
    def get_readings(self):
        ''' Reads sensor values from Serial and updates self.distances.  Also applies 
            distance cutoffs
        '''
        # get sensor readings
        readings = self.ser.read()
        
        # parse readings
        if len(readings) == self.num_sensors:
            self.distances = [float(r + str(0)) for r in readings] # convert to float
        
        # apply distance cutoffs
        self.distances = [min(d, self.cutoff) for d in self.distances]
        
        # return distances
        return self.distances
        
    def check_distances(self):
        ''' Returns list of bools.  True means threshold has been met. '''
        _ = self.get_readings()
        
        return [int(d <= self.thresh) for d in self.distances]
        
class IRSensor(object):
    def __init__(self, ser):
        self.ser = ser #serial wrapper
        self.num_sensors = config.numIRSensors
        self.sensors = config.irSensors
        self.thresh = config.irThreshold
        self.mins = config.irMins
        self.maxs = config.irMaxs
        self.error_weights = config.irError
        self.correction_weights = config.corrections
        
    def get_readings(self):
        ''' Returns analog sensor readings '''
        # get sensor readings
        readings = self.ser.read()
        
        # parse readings
        if len(readings) == self.num_sensors:
            self.sensors = [int(x +str(0)) / 10 for x in readings]
            
        # return sensor readings
        return self.sensors
            
    def update_limits(self, values):
        ''' Updates min/max limits if values[i] outside of mins[i] or maxs[i] '''
        
        for i in range(self.num_sensors):
            self.mins[i] = min(self.mins[i], values[i])
            self.maxs[i] = max(self.maxs[i], values[i])
            
    def calculate_correction(self, mode = 'basic', pid=None):
        ''' Returns correction tuple of the format:
                (mathematical operator, left speed adjustment, right speed adjustment). 
            Parameters:
                mode: str - 'basic'  --> applies correction_weights, 'pid' --> applies PID(error)
                pid: PID object (default None) 
        '''
        
        # Get Readings
        values = self.get_readings()

        # Initialize defaults (i.e. no adjustment)       
        if mode == 'basic': # subtracts correction
            leftadj = 0
            rightadj = 0
            operator = operator.sub
        else:
            operator = operator.mul
            leftadj = 1
            rightadj = 1

        # Loop through sensors and find the first that exceeds boundary
        for i, v, mx, ew, cw in zip(range(self.num_sensors, values, self.maxs, self.error_weights, self.correction_weights):
            if mx-self.thresh <= v <= mx+thresh:
                if mode == 'basic': 
                    if i < self.num_sensors/2:
                        leftadj = cw
                    else:
                        rightadj = cw
                else:
                    if i < self.num_sensors/2:
                        leftadj = pid.output(ew)
                    else:
                        rightadj = pid.output(ew)
                break
                
        return (operator, leftadj, rightadj)
        
class PID(object):
    
    def __init__(self, target = 0, kp = 1, ki = 1, kd = 1):
        self.target = target
        self.lastTime = int(round(time.time()*1000)-1) 
        self.sumError = 0
        self.lastError = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
    
    def output(err):
        ''' Calculates PID output correction '''
    
        
        # get the current time 
        now = int(round(time.time()*1000)) 
        duration = now - self.lastTime 
        
        # calculate the error 
        error = self.target - err 
        self.sumError += (error * duration) 
        dError = (error - self.lastError)/duration
        
        # calculate PID 
        output = self.kp * error + self.ki * self.sumError + self.kd * dError 
        
        # update variables 
        self.lastError = error 
        self.lastTime = now
    
        # return the output value 
        return output 
        
