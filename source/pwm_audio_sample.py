from machine import Pin, Timer, freq, PWM
import utime
from fm_radio import Radio
import sample

class PWM_Audio():
    def __init__(self):
        self.loop_lim = len(sample.WAV_DATA)
        self.audio = PWM(Pin(10, Pin.OUT))
        self.index = 0
        self.duty_cycle = 0
        self.timer = Timer()

    def pwm_interupt(self, t):
        self.audio.duty_u16(self.duty_cycle)
        if(self.index >= self.loop_lim-1):
            self.index=0
        else: self.index += 1
        self.duty_cycle = sample.WAV_DATA[self.index]*256
        pass

    def pwm_start(self):
        self.audio.freq(40000)
        self.timer.init(mode=Timer.PERIODIC, freq=4000, callback=self.pwm_interupt)

    def pwm_stop(self):
        self.timer.deinit()
        self.audio.deinit()

# radio = Radio(101.9, 1, True)

# audio = PWM_Audio()

# audio.pwm_start()


# while True:
#     pass
