from menu import Menu
from rotary import Encoder
from ssd1306 import SSD1306_SPI
from fm_radio import Radio
from machine import Pin, Timer
import utime
from screens import Screen

volume_encoder = Encoder(18, 17)
selection_encoder = Encoder(27, 26)

select_button = Pin(28, Pin.IN, Pin.PULL_UP)
snooze_button = Pin(16, Pin.IN, Pin.PULL_UP)

radio = Radio(101.9, 2, False)

menu = Menu(radio, volume_encoder, selection_encoder, select_button, snooze_button)
screen = Screen()

while True: 
    utime.sleep_ms(1)
    screen.standby(menu.get_time, menu.get_date,0,1)
    menu.update()
    


