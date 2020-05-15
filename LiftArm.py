import ev3dev.ev3 as ev3
from time import sleep

def liftUp(lf):
    lf.polarity = "normal"
    lf.run_forever(speed_sp=50)
    sleep(1.5)
    lf.stop()


def liftDown(lf):
    lf.polarity = "inversed"
    lf.run_forever(speed_sp=50)
    sleep(1.5)
    lf.stop()

def forward(lm, rm):
    lm.polarity = "normal"
    rm.polarity = "normal"
    lm.run_forever(speed_sp=100)
    rm.run_forever(speed_sp=100)
    sleep(2)
    lm.stop()
    rm.stop()

def backward(lm, rm, time):
    lm.polarity = "inversed"
    rm.polarity = "inversed"
    lm.run_forever(speed_sp=100)
    rm.run_forever(speed_sp=100)
    sleep(time)
    lm.stop()
    rm.stop()


if __name__ == "__main__":
    rm = ev3.LargeMotor('outC')
    lm = ev3.LargeMotor('outB')
    lf = ev3.MediumMotor('outA')
    assert rm.connected
    assert lm.connected
    assert lf.connected
    forward(lm, rm)
    liftUp(lf)
    backward(lm, rm, 2)
    liftDown(lf)
    backward(lm, rm, 1)
