

# PID 
sensorErr = 0 
lastTime = int(round(time.time()*1000)) 
lastError = 0 
target = 0 

kp = 0.5
ki = 0.5 
kd = 1 

#4. Create the PID function. 
def PID(err): 
    # check if variables are defined before use 
    # the first time the PID is called these variables will
    # not have been defined 
    try: lastTime 
    except NameError: lastTime = int(round(time.time()*1000)-1) 
    
    try: sumError 
    except NameError: sumError = 0 
    
    try: lastError 
    except NameError: lastError = 0
    
    # get the current time 
    now = int(round(time.time()*1000)) 
    duration = now-lastTime 
    
    # calculate the error 
    error = target - err 
    sumError += (error * duration) 
    dError = (error - lastError)/duration
    
    # calculate PID 
    output = kp * error + ki * sumError + kd * dError 
    
    # update variables 
    lastError = error 
    lastTime = now

    # return the output value 
    return output 
    
    
#5. Replace the followLine function with this: 
def followLine(): 
    leftSpeed = speedDef 
    rightSpeed = speedDef 
    
    getIR() 
    
    prString = '' 
    for x in range(5): 
        prString += ('IR' + str(x) + ': ' + str(irSensors[x]) + ' ') 
    print prString 
    
    # find line and correct if necessary 
    if(irMaxs[0]-irThresh <= irSensors[0] <= irMaxs[0]+irThresh): 
        sensorErr = 2 
    elif(irMaxs[1]-irThresh <= irSensors[1] <= irMaxs[1]+irThresh): 
        sensorErr = 1 
    elif(irMaxs[3]-irThresh <= irSensors[3] <= irMaxs[3]+irThresh): 
        sensorErr = -1 
    elif(irMaxs[4]-irThresh <= irSensors[4] <= irMaxs[4]+irThresh): 
        sensorErr = -2 
    else: 
        sensorErr = 0


    # get PID results 
    ratio = PID(sensorErr) 
    
    # apply ratio 
    leftSpeed = speedDef * ratio 
    rightSpeed = speedDef * -ratio 
    
    # drive the motors 
    driveMotors(leftSpeed, rightSpeed, driveTime)

