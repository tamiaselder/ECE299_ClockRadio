from menu import Menu, Screens, ClockSettings, AlarmSettings
from rotary import Encoder
from ssd1306 import SSD1306_SPI
from fm_radio import Radio
from machine import Pin, Timer, freq
import utime
from screens import Screen

machine.freq(270000000)

volume_encoder = Encoder(18, 17)
selection_encoder = Encoder(26, 27)

select_button = Pin(28, Pin.IN, Pin.PULL_UP)
snooze_button = Pin(16, Pin.IN, Pin.PULL_UP)

screen = Screen()
radio = Radio(101.9, 0, True)

menu = Menu(radio, volume_encoder, selection_encoder, select_button, snooze_button)

while True: 
    menu.update()
    if(menu.alarm_triggered()):
        screen.alarm(menu.get_snooze())
    elif(menu.get_screen() == Screens.STANDBY):
        screen.standby(
            menu.get_time(), 
            menu.get_time_format(),
            menu.get_date(),
            menu.get_alarm_hour(),
            menu.get_alarm_min(),
            menu.get_alarm_set(),
            menu.get_station())
    elif(menu.get_screen() == Screens.TIME_MENU):
        screen.time_menu(
            menu.get_time(),
            menu.get_date(),
            menu.get_alarm_set(),
            menu.get_alarm_hour(),
            menu.get_alarm_min(),
            menu.get_time_format())
        if(menu.in_screen() == True):
            if(menu.get_option() == ClockSettings.TIME_HOUR):
                screen.hlt_time_hr()
            elif(menu.get_option() == ClockSettings.TIME_MIN):
                screen.hlt_time_min()
            elif(menu.get_option() == ClockSettings.TIME_FORMAT):
                screen.hlt_clkmd()
            elif(menu.get_option() == ClockSettings.ALARM_HOUR):
                screen.hlt_alrm_hr()
            elif(menu.get_option() == ClockSettings.ALARM_MIN):
                screen.hlt_alrm_min()
            elif(menu.get_option() == ClockSettings.ALARM_SET):
                screen.hlt_alrmst()

    elif(menu.get_screen() == Screens.ALARM_MENU):
        screen.alarm_menu(
            menu.get_alarm_vol(),
            menu.get_snooze_time(),
            menu.get_alarm_tone(),
            menu.get_snooze())
        if(menu.in_screen() == True):
            if(menu.get_option() == AlarmSettings.ALARM_TONE):
                screen.hlt_sound()
            elif(menu.get_option() == AlarmSettings.ALARM_VOL):
                screen.hlt_vol()
            elif(menu.get_option() == AlarmSettings.SNOOZE_TIME):
                screen.hlt_snooze_time()
    
    elif(menu.get_screen() == Screens.FACE):
        screen.face()

    elif(menu.get_screen() == Screens.RADIO_MENU):
        screen.radio_menu(
            menu.get_station(), 
            "Moosic", 
            menu.get_volume())
    

        


