from machine import Pin, I2C, Timer

A_state = [0, 0, 0]
B_state = [0, 0, 0]


Vol = 0

def encoderA_callback(pin):
    global B_state, A_state, Vol
    state = pin.irq().flags()
    A_state[2] = 1 
    if(state == B_state[0] and A_state[0] == B_state[1] and B_state[2]):
        Vol = Vol + 1 if Vol < 30 else 0
        print(Vol)
        B_state[2] = 0
        A_state[2] = 0
    A_state[1] = A_state[0]
    A_state[0] = state


def encoderB_callback(pin):
    global B_state, A_state, Vol
    state = pin.irq().flags()
    B_state[2] = 1
    if(state == A_state[0] and B_state[0] == A_state[1] and A_state[2]):
        Vol = Vol - 1 if Vol > 0 else 30
        print(Vol)
        A_state[2] = 0
        B_state[2] = 0
    B_state[1] = B_state[0]
    B_state[0] = state



encoder_A = Pin(19, Pin.IN)
encoder_B = Pin(18, Pin.IN)

encoder_A.irq(encoderA_callback, Pin.IRQ_FALLING | Pin.IRQ_RISING)
encoder_B.irq(encoderB_callback, Pin.IRQ_FALLING | Pin.IRQ_RISING)

timA = Timer()
timB = Timer()

while True:
    pass