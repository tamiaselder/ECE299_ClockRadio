from fm_radio import Radio
from rotary import Encoder
from machine import RTC, Pin, Timer
from pwm_audio import PWM_Audio

class ClockSettings:
    TIME_HOUR = 0
    TIME_MIN = 1
    TIME_FORMAT = 2
    ALARM_HOUR = 3
    ALARM_MIN = 4
    ALARM_SET = 5

class AlarmSettings:
    ALARM_TONE = 0
    ALARM_VOL = 1
    SNOOZE_TIME = 2

class Screens:
    STANDBY = 0
    TIME_MENU = 1
    ALARM_MENU = 2
    RADIO_MENU = 3


class Menu():
    def __init__(self, radio: Radio, vol_encoder: Encoder, selection_endcoder: Encoder, selection_button: Pin, reset_button: Pin):
        self._radio = radio

        self._current_screen = Screens.STANDBY
        self._current_option = 0

        self._in_screen = 0
        self._in_option = 0

        self._rtc = RTC()
        self._audio = PWM_Audio()

        self._alarm_time = [12, 0]
        self._alarm_triggered = False
        self._alarm_set = 0
        self._alarm_tone = 0
        self._alarm_vol = 0
        self._snooze_time = 5

        self._time_format_24 = 1

        self._vol_encoder = vol_encoder
        self._selection_encoder = selection_endcoder

        self._selection_button = selection_button
        self._reset_button = reset_button

        self._selection_button_timer = Timer()
        self._reset_button_timer = Timer()
        self._snooze_timer = Timer()
    
        self._snooze_on = 0

        self._vol_encoder.set_update_val(self._radio.GetSettings()[1], 0, 15)
        self._selection_encoder.set_update_val(0, 0, 3)

        self._selection_button.irq(self._selection_button_callback, Pin.IRQ_RISING)
        self._reset_button.irq(self._reset_button_callback, Pin.IRQ_RISING)
        
        self._previous_value = 0



    def update(self):
        vol = self._vol_encoder.value()
        if(vol == 0 and vol != self.get_volume()):
            self._radio.SetVolume(0)
            self._radio.SetMute(True)
            self._radio.ProgramRadio()
        elif(vol != self.get_volume()):
            self._radio.SetMute(False)
            self._radio.SetVolume(vol)
            self._radio.ProgramRadio()
        
        time = self._rtc.datetime()[4:8]
        if(self._alarm_time[0] == time[0] and self._alarm_time[1] == time[1] and time[2] == 0 and self._alarm_set == 1):
            self._radio.SetMute(True)
            self._radio.UpdateSettings()
            self._radio.ProgramRadio()
            self._alarm_triggered = True
            self._alarm_set = 0            
            self._selection_encoder.set_update_val(0, 0, 1)
            self._selection_encoder.set_update_increment(1)
            self._audio.reinit(self._alarm_tone)
            self._audio.pwm_start(self._alarm_vol)

        value = self._selection_encoder.value()
        if(value != self._previous_value):
            if(self._alarm_triggered):
                self._snooze_on = value

            elif(not self._in_screen):
                self._current_screen = value

            elif(self._in_screen and not self._in_option):
                if(self._current_screen == Screens.TIME_MENU):
                    self._current_option = value
                elif(self._current_screen == Screens.RADIO_MENU):
                    self._radio.SetFrequency(value)
                    self._radio.UpdateSettings()
                    self._radio.ProgramRadio()
                elif(self._current_screen == Screens.STANDBY):
                    pass
            
            elif(self._in_option and self._current_screen == Screens.TIME_MENU):
                if(self._current_option == ClockSettings.TIME_HOUR):
                    self.set_time_hour(value)
                elif(self._current_option == ClockSettings.TIME_MIN):
                    self.set_time_minute(value)
                elif(self._current_option == ClockSettings.TIME_FORMAT):
                    self._time_format_24 = value
                elif(self._current_option == ClockSettings.ALARM_SET):
                    self._alarm_set = value
                elif(self._current_option == ClockSettings.ALARM_MIN):
                    self._alarm_time[1] = value
                elif(self._current_option == ClockSettings.ALARM_HOUR):
                    self._alarm_time[0] = value
            
            elif(self._in_option and self._current_screen == Screens.ALARM_MENU):
                if(self._current_option == AlarmSettings.ALARM_TONE):
                    self._alarm_tone = value
                elif(self._current_option == AlarmSettings.ALARM_VOL):
                    self._alarm_vol = value
                elif(self._current_option == AlarmSettings.SNOOZE_TIME):
                    self._snoooze_time = value
        
        self._previous_value = value

    def _reset_button_callback(self,pin):
        self._reset_button_timer.init(mode=Timer.ONE_SHOT, period=10, callback=self._reset_button_timer_callback)

    def _reset_button_timer_callback(self, pin):
        if(self._in_screen and not self._in_option):
            self._in_screen = False
            self._selection_encoder.set_update_val(self._current_screen, 0, 2)
            self._selection_encoder.set_update_increment(1)

    def _selection_button_callback(self,pin):
        self._reset_button_timer.init(mode=Timer.ONE_SHOT, period=10, callback=self._selection_button_timer_callback)

    def _selection_button_timer_callback(self,pin):
        if(self._alarm_triggered == True):
            if self._snooze_on == 1 :
                self._snooze_timer.init(mode=Timer.ONE_SHOT, period=self._snooze_time * 6000, callback=self._snooze_timer_callback)
            self._alarm_triggered = False
            self._in_screen = False
            self._in_option = False
            if(self.get_volume() != 0):
                self._radio.SetMute(False)
                self._radio.UpdateSettings()
                self._radio.ProgramRadio()
            self._selection_encoder.set_update_increment(1)
            self._selection_encoder.set_update_val(self._current_screen, 0, 2)
            self._alarm_set = 1
            self._audio.pwm_stop()

        elif(not self._in_option and self._in_screen and self._current_screen == Screens.TIME_MENU):
            self._in_option = True
            if(self._current_option == ClockSettings.TIME_HOUR):
                self._selection_encoder.set_update_val(self.get_time()[0], 0, 23)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == ClockSettings.TIME_MIN):
                self._selection_encoder.set_update_val(self.get_time()[1], 0, 59)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == ClockSettings.TIME_FORMAT):
                self._selection_encoder.set_update_val(self._time_format_24, 0, 1)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == ClockSettings.ALARM_SET):
                self._selection_encoder.set_update_val(self._alarm_set, 0, 1)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == ClockSettings.ALARM_MIN):
                self._selection_encoder.set_update_val(self._alarm_time[1], 0, 59)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == ClockSettings.ALARM_HOUR):
                self._selection_encoder.set_update_val(self._alarm_time[0], 0, 23)
                self._selection_encoder.set_update_increment(1)
        
        elif(not self._in_option and self._in_screen and self._current_screen == Screens.ALARM_MENU):
            self._in_option = True
            if(self._current_option == AlarmSettings.ALARM_TONE):
                self._selection_encoder.set_update_val(self._alarm_tone, 0, 2)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == AlarmSettings.ALARM_VOL):
                self._selection_encoder.set_update_val(self._alarm_vol, 1, 20)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_option == AlarmSettings.SNOOZE_TIME):
                self._selection_encoder.set_update_val(self._snooze_time, 1, 20)
                self._selection_encoder.set_update_increment(1)
    
        elif(self._in_option):
            self._in_option = False
            if(self._current_screen == Screens.TIME_MENU):
                self._selection_encoder.set_update_val(self._current_option, 0, 5)
            elif(self._current_screen == Screens.ALARM_MENU):
                self._selection_encoder.set_update_val(self._current_option, 0, 2)
            self._selection_encoder.set_update_increment(1)

        elif(not self._in_screen):
            self._in_screen = True
            if(self._current_screen == Screens.TIME_MENU):
                self._selection_encoder.set_update_val(self._current_option, 0, 5)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_screen == Screens.ALARM_MENU):
                self._selection_encoder.set_update_val(self._current_option, 0, 2)
                self._selection_encoder.set_update_increment(1)
            elif(self._current_screen == Screens.RADIO_MENU):
                self._selection_encoder.set_update_val(self.get_station(), 88, 108)
                self._selection_encoder.set_update_increment(0.1)
            elif(self._current_screen == Screens.STANDBY):
                pass

    def _snooze_timer_callback(self, pin):
        if(self._alarm_set == 1):
            self._alarm_triggered = True
            self._radio.SetMute(True)
            self._radio.UpdateSettings()
            self._radio.ProgramRadio()
            self._selection_encoder.set_update_val(0, 0, 1)
            self._selection_encoder.set_update_increment(1)
            self._audio.reinit(self._alarm_tone)
            self._audio.pwm_start(self._alarm_vol)

    def get_screen(self):
        return self._current_screen

    def get_option(self):
        return self._current_option
    
    def get_station(self):
        return self._radio.GetSettings()[2]
    
    def get_volume(self):
        return self._radio.GetSettings()[1]

    def get_time(self):
        time = self._rtc.datetime()
        if(not self._time_format_24 and (time[4] > 12 or time[4] == 0)):
            return (
                12 if time[4] == 0 else time[4] - 12, 
                time[5], 
                time[6], 
                time[7])
        return (time[4], time[5], time[6], time[7])
    
    def set_time_hour(self, hour):
        time = self.get_time()
        date = self.get_date()
        self._rtc.datetime([date[0], date[1], date[2], date [3], hour, time[1], time[2], time[3]])
    
    def set_time_minute(self, minute):
        time = self.get_time()
        date = self.get_date()
        if(not self._time_format_24):
            self._rtc.datetime([
                date[0], 
                date[1], 
                date[2], 
                date [3], 
                time[0] + 12, 
                minute, 
                time[2], 
                time[3]])
        self._rtc.datetime([date[0], date[1], date[2], date [3], time[0], minute, time[2], time[3]])
    
    def get_date(self):
        date = self._rtc.datetime()
        return (date[0], date[1], date[2], date[3])
    
    def set_alarm_state(self, state: bool):
        self._alarm_triggered = state
    
    def enable_alarm(self, state: bool):
        self._alarm_set = state

    def set_alarm_hour(self, hour):
        self._alarm_time[0] = hour

    def set_alarm_min(self, minute):
        self._alarm_time[1] = minute
    
    def get_alarm_hour(self):
        return self._alarm_time[0]

    def get_alarm_min(self):
        return self._alarm_time[1]
    
    def get_time_format(self):
        return self._time_format_24
    
    def get_alarm_set(self):
        return self._alarm_set
    
    def in_screen(self):
        return self._in_screen
    
    def in_option(self):
        return self._in_option
    
    def alarm_triggered(self):
        return self._alarm_triggered

    def get_snooze(self):
        return self._snooze_on

    def get_snooze_time(self):
        return self._snooze_time
    
    def get_alarm_tone(self):
        return self._alarm_tone
    
    def get_alarm_vol(self):
        return self._alarm_vol