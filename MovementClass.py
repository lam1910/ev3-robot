#!/usr/bin/env python3
from time import sleep

class MovementController:

    def __init__(self, leftMotor, rightMotor):
        #set wheel motor for MovementController
        self.leftMotor = leftMotor;
        self.rightMotor = rightMotor
        #set up connection
        assert self.leftMotor.connected
        assert self.rightMotor.connected

    #set motor to rotate clock-wise
    def setNormal(self):
        self.leftMotor.polarity = "normal"
        self.rightMotor.polarity = "normal"

    #set motor to rotate counter clock-wise
    def setInverse(self):
        self.leftMotor.polarity = "inversed"
        self.rightMotor.polarity = "inversed"

    def setRightSpeed(self, speed):
        self.rightMotor.run_forever(speed_sp=speed)

    def setLeftSpeed(self, speed):
        self.leftMotor.run_forever(speed_sp=speed)

    def setLeftInverse(self):
        self.leftMotor.polarity = "inversed"

    def setRightInverse(self):
        self.rightMotor.polarity = "inversed"

    def setSpeed(self, speed):
        self.leftMotor.run_forever(speed_sp=speed)
        self.rightMotor.run_forever(speed_sp=speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    #reset all the config
    def reset(self):
        self.leftMotor.reset()
        self.rightMotor.reset()

    #set robot to run forward with speed of 100
    def forward(self):
        self.leftMotor.run_forever(speed_sp=300)
        self.rightMotor.run_forever(speed_sp=300)

    #set robot to run backward with speed of 100
    # def backward(self):
    #     setInverse()
    #     self.leftMotor.run_forever(speed_sp=100)
    #     self.rightMotor.run_forever(speed_sp=100)

    #set robot to turn left
    def turnLeft(self):
        self.leftMotor.run_forever(speed_sp=70)
        self.rightMotor.run_forever(speed_sp=400)

    #set robot to turn right
    def turnRight(self):
        self.leftMotor.run_forever(speed_sp=400)
        self.rightMotor.run_forever(speed_sp=70)
