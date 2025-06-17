from machine import Pin, I2C, Timer

A_state = [0, 0]
B_state = [0, 0]


Vol = 0

def timA_callback(pin):
    global A_state, B_state, Vol
    if(A_state[0] == B_state[0] and A_state[0] == B_state[1]):
        Vol = Vol - 1 if Vol > 0 else 15
        print(Vol)

def timB_callback(pin):
    global A_state, B_state, Vol
    if(A_state[0] == B_state[0] and A_state[1] == B_state[1]):
        Vol = Vol + 1 if Vol < 15 else 0
        print(Vol)

def encoderA_callback(pin):
    global A_state
    A_state[1] = A_state[0]
    A_state[0] = pin.irq().flags()
    timA.init(mode=Timer.ONE_SHOT, period=3, callback=timA_callback)


def encoderB_callback(pin):
    global B_state
    B_state[1] = B_state[0]
    B_state[0] = pin.irq().flags()
    timB.init(mode=Timer.ONE_SHOT, period=3, callback=timB_callback)



encoder_A = Pin(19, Pin.IN)
encoder_B = Pin(18, Pin.IN)

encoder_A.irq(encoderA_callback, Pin.IRQ_FALLING | Pin.IRQ_RISING)
encoder_B.irq(encoderB_callback, Pin.IRQ_FALLING | Pin.IRQ_RISING)

timA = Timer()
timB = Timer()
