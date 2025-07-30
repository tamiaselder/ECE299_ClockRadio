from machine import Pin, I2C, Timer
from utime import sleep

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
        self._limit_min = 0
        self._limit_max = 0
        self._increment = 1


    def _encoder_a_callback(self, pin):
        state = pin.irq().flags()
        self._a_state[2] = 1 
        if(state == self._b_state[0] and self._a_state[0] == self._b_state[1] and self._b_state[2]):
            self._cw_count += 1
            if(self._cw_count == 2):
                self._current_update_value = self._current_update_value + self._increment if self._current_update_value < self._limit_max else self._limit_min
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
                self._current_update_value = self._current_update_value - self._increment if self._current_update_value > self._limit_min else self._limit_max
                self._ccw_count = 0
            self._a_state[2] = 0
            self._b_state[2] = 0
        self._b_state[1] = self._b_state[0]
        self._b_state[0] = state
    
    def set_update_val(self, x, limit_min, limit_max):
        self._current_update_value = x
        self._limit_min = limit_min
        self._limit_max = limit_max

    def set_update_increment(self, inc):
        self._increment = inc

    def value(self):
        return self._current_update_value
