from machine import Pin, Timer, freq, PWM
import utime
from weezer import WAV_DATA

class PWM_Audio():
    def __init__(self):
        self.loop_lim = len(WAV_DATA)
        self.audio = PWM(Pin(10, Pin.OUT))
        self.index = 0
        self.duty_cycle = 0
        self.timer = Timer()

    def pwm_interupt(self, t):
        self.audio.duty_u16(self.duty_cycle)
        if(self.index >= self.loop_lim-1):
            self.index=0
        else: self.index += 1
        self.duty_cycle = WAV_DATA[self.index]*256
        pass

    def pwm_start(self):
        self.audio.freq(80000)
        self.timer.init(mode=Timer.PERIODIC, freq=8000, callback=self.pwm_interupt)

    def pwm_stop(self):
        self.timer.deinit()
        self.audio.deinit()

audio = PWM_Audio()
audio.pwm_start()

utime.sleep(10)

audio.pwm_stop()