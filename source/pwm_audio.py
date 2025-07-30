from machine import Pin, Timer, freq, PWM
import utime
from fm_radio import Radio
import sample
import uasyncio as asyncio

class PWM_Audio():
    def __init__(self):
        self.loop_lim = len(sample.WAV_DATA)
        self.audio = PWM(Pin(10, Pin.OUT))
        self.index = 0
        self.duty_cycle = 0
        self.timer = Timer()

    def pwm_interupt(self, t):
        if (sample.WAV_DATA[self.index][0] > 10):
            self.audio.freq(int(sample.WAV_DATA[self.index][0]))  
        else:
            self.audio.deinit()
        self.timer.init(mode=Timer.ONE_SHOT, period = sample.WAV_DATA[self.index][1], callback=self.pwm_interupt)
        if(self.index >= self.loop_lim-1):
            self.index=0
        else: self.index += 1
        pass

    def pwm_start(self):
        self.audio.duty_u16(1000)
        self.timer.init(mode=Timer.ONE_SHOT, period = 1, callback=self.pwm_interupt)

    def pwm_stop(self):
        self.timer.deinit()
        self.audio.deinit()
