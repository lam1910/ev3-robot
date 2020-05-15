#!/usr/bin/env python3
from time import sleep

class ArmController:

    def __init__(self, middleMotor):
        #set arm motor for ArmController
        self.middleMotor = middleMotor;
        assert self.middleMotor.connected

    def pickUp(self):
        self.middleMotor.polarity = "normal" # this will make the motor rotates clock-wise, which means going up
        self.middleMotor.run_forever(speed_sp=50) # speed 50 is pretty enough to lift package up
        sleep(1.3) # wait until the arm reach certain high.
        self.middleMotor.stop() # stop rotates
        self.middleMotor.reset() # reset the config

    def putDown(self):
        self.middleMotor.polarity = "inversed" # this will make the motor rotates clock-wise, which means going down
        self.middleMotor.run_forever(speed_sp=50) # speed 50 is pretty enough to lift package up
        sleep(1.3) # wait until the robot lower its arm to drop the package.
        self.middleMotor.stop() # stop rotates
        self.middleMotor.reset() # reset the config
