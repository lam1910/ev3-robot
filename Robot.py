#!/usr/bin/env python3
from time import sleep
import ev3dev.ev3 as ev3
import RoutingClass as Route
import ArmClass as Arm
import MovementClass as Movement
import bluetooth
import ast

hostMACAddress = '00:17:E9:F8:72:06' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)

class Robot():
    def __init__(self, currentPos, path, action, gs, cs, mc, ac, rc):
        #set wheel motor for MovementController
        self.currentPos = currentPos
        self.path = path
        self.action = action
        self.cs = cs
        self.gs = gs
        self.mc = mc
        self.ac = ac
        self.rc = rc

    def lineFollowing(self):
        self.mc.setNormal()
        stop = False
        while not stop:
            if (self.cs.value() == 6):
                self.mc.turnLeft()
            elif (self.cs.value() == 1):
                self.mc.turnRight()
            self.mc.setSpeed(300)
            if (self.cs.value() == 5):
                self.mc.stop()
                self.processAction()
                if (len(self.path) == 0 and len(self.action) == 0):
                    stop = True

            if (self.cs.value() == 3):
                self.mc.setSpeed(300)
                self.processRoute()


    def processRoute(self):
        print(self.path)
        if self.path[0] == "left":
            self.turnLeft(78)
        elif self.path[0] == "right":
            self.turnRight(87)
        else:
            self.forward()
            sleep(0.7)
        self.path.pop(0)

    def processAction(self):
        if (len(self.action) > 0):
            print(self.action[0])
            if self.action[0] == "Pick Up":
                self.ac.pickUp()
            elif self.action[0] == "Put Down":
                self.ac.putDown()
                self.mc.setInverse()
                self.forward()
                self.mc.setNormal()
            self.action.pop(0)

        self.turnAround(180)

    def turnAround(self, degree):
        self.mc.setRightInverse()
        self.mc.setLeftSpeed(200)
        self.mc.setRightSpeed(200)
        self.gs.mode = "GYRO-RATE"
        self.gs.mode = "GYRO-ANG"
        tmp = self.gs.value()
        while(abs(self.gs.value() - tmp) <= degree):
            # print("tmp: ",tmp)
            # print("value: ",self.gs.value())
            # print(abs(self.gs.value() - tmp))
            pass
        self.mc.setNormal()
        self.mc.stop()

    def forward(self):
        # sleep(0.4)
        self.mc.forward()
        sleep(0.5)

    def turnRight(self, degree):
        sleep(0.13)
        tmp = self.gs.value()
        while(abs(self.gs.value() - tmp) <= degree):
            self.mc.setLeftSpeed(200)
            self.mc.setRightSpeed(0)

    def turnLeft(self, degree):
        sleep(0.15)
        tmp = self.gs.value()
        self.mc.setLeftInverse()
        while(abs(self.gs.value() - tmp) <= degree):
            # mc.turnLeft()
            self.mc.setLeftSpeed(0)
            self.mc.setRightSpeed(200)
        self.mc.setNormal()

    def addRoute(self, start, end):
        if start == "":
            start = self.currentPos
        self.path += self.rc.findPath(start, end)
        self.currentPos = end
    def getRoute(self):
        return self.path

    def addAction(self, action):
        self.action += action

    def receiveCommand(self, commands):
        for command in commands:
            for location, action in command.items():
                if (location == self.currentPos):
                    self.reset()
                    return False
                self.addRoute('', location)
                self.addAction([action])
        return True

    def reset(self):
        self.path = []
        self.action = []

    def reload(self):
        self.reset()
        self.currentPos = "Start"

    def stop(self):
        self.mc.stop()

    def start(self):
        self.lineFollowing()

if __name__ == "__main__":

    done = False
    rm = ev3.LargeMotor('outC')
    lm = ev3.LargeMotor('outB')
    lf = ev3.MediumMotor('outA')
    gs = ev3.GyroSensor()
    cs = ev3.ColorSensor()

    mc = Movement.MovementController(lm, rm)
    ac = Arm.ArmController(lf)
    rc = Route.RoutingController('', '')

    # action = ["pickup", "putdown", "pickup", "putdown"]
    assert cs.connected
    assert gs.connected
    cs.mode = "COL-COLOR"
    gs.mode = "GYRO-ANG"

    robot = Robot("Start", [], [], gs, cs, mc, ac, rc)

    while not done:
        try:
            print("Waiting for Ev3-App connection")
            client, clientInfo = s.accept()
            print("Ev3-App Conntected\nWaiting for command")
            while 1:
                data = client.recv(size)
                if data:
                    commands = ast.literal_eval(data.decode("ascii"))
                    #format of data: a:b
                    robot.reset()
                    print(commands)
                    if (robot.receiveCommand(commands)):
                        robot.start()
                        print("Job Done!")
                        client.send("done") # Echo back to client
                    else:
                        client.send("refuse")

        except KeyboardInterrupt:
            robot.stop()
            print("\nShut down the robot\n")
            done = True
            client.close()
            s.close()

        except bluetooth.btcommon.BluetoothError:
            robot.stop()
            print("Connection lost! Closing Ev3-App socket!")
            robot.reset()
            client.close()

        except:
            robot.stop()
            print("Something wrong happens! Please reset the robot to starting point")
            robot.reload()
            client.close()

    # try:
    #     robot.addRoute('','d')
    #     robot.addRoute('', 'a')
    #     robot.addRoute('', 'c')
    #     robot.addRoute('', 'b')
    #     robot.addRoute('', 'start')
    #     print (robot.getRoute())
    #     robot.lineFollowing()
    #     mc.stop()
    #     # ac.pickUp()
    #     # mc.stop()
    # except KeyboardInterrupt:
    #     mc.stop()
    # except:
    #     mc.stop()

    #red: 5
    #black: 1
    #white: 6
    #blue: 2
    #green: 3
