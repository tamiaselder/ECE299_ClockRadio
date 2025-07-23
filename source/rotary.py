from machine import Pin, I2C, Timer
from utime import sleep

# A_state = [0, 0, 0]
# B_state = [0, 0, 0]


# Vol = 0

# def encoderA_callback(pin):
#     global B_state, A_state, Vol
#     state = pin.irq().flags()
#     A_state[2] = 1 
#     if(state == B_state[0] and A_state[0] == B_state[1] and B_state[2]):
#         Vol = Vol + 1 if Vol < 30 else 0
#         print(Vol)
#         B_state[2] = 0
#         A_state[2] = 0
#     A_state[1] = A_state[0]
#     A_state[0] = state


# def encoderB_callback(pin):
#     global B_state, A_state, Vol
#     state = pin.irq().flags()
#     B_state[2] = 1
#     if(state == A_state[0] and B_state[0] == A_state[1] and A_state[2]):
#         Vol = Vol - 1 if Vol > 0 else 30
#         print(Vol)
#         A_state[2] = 0
#         B_state[2] = 0
#     B_state[1] = B_state[0]
#     B_state[0] = state



# encoder_A = Pin(18, Pin.IN)
# encoder_B = Pin(17, Pin.IN)

# encoder_A.irq(encoderA_callback, Pin.IRQ_FALLING|Pin.IRQ_RISING)
# encoder_B.irq(encoderB_callback, Pin.IRQ_FALLING|Pin.IRQ_RISING)

# timA = Timer()
# timB = Timer()

class Encoder():
    def __init__(self, pin_a, pin_b):
        self._encoder_A = Pin(pin_a, Pin.IN)
        self._encoder_B = Pin(pin_b, Pin.IN)

        self._encoder_A.irq(self._encoder_a_callback, Pin.IRQ_RISING|Pin.IRQ_FALLING)
        self._encoder_B.irq(self._encoder_b_callback, Pin.IRQ_RISING|Pin.IRQ_FALLING)

        self._a_state = [0, 0, 0]
        self._b_state = [0, 0, 0]

        self._cw_count = 0
        self._ccw_count = 0

        self._current_update_value = 0
        self._update_value_limit = 0

    def _encoder_a_callback(self, pin):
        state = pin.irq().flags()
        self._a_state[2] = 1 
        if(state == self._b_state[0] and self._a_state[0] == self._b_state[1] and self._b_state[2]):
            self._cw_count += 1
            if(self._cw_count == 2):
                self._current_update_value = self._current_update_value + 1 if self._current_update_value < self._update_value_limit else 0
                print(self._current_update_value)
                self._cw_count = 0
            self._b_state[2] = 0
            self._a_state[2] = 0
        self._a_state[1] = self._a_state[0]
        self._a_state[0] = state
    
    def _encoder_b_callback(self, pin):
        state = pin.irq().flags()
        self._b_state[2] = 1
        if(state == self._a_state[0] and self._b_state[0] == self._a_state[1] and self._a_state[2]):
            self._ccw_count += 1
            if(self._ccw_count == 2):
                self._current_update_value = self._current_update_value - 1 if self._current_update_value > 0 else self._update_value_limit
                print(self._current_update_value)
                self._ccw_count = 0
            self._a_state[2] = 0
            self._b_state[2] = 0
        self._b_state[1] = self._b_state[0]
        self._b_state[0] = state
    
    def set_update_val(self, x, limit):
        self._current_update_value = x
        self._update_value_limit = limit
    
    def value(self):
        return self._current_update_value

encoder = Encoder(18, 17)

vol = [1]
encoder.set_update_val(vol, 30)

while True:
    sleep(1)
    # print(vol)