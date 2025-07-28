from menu import Menu
from rotary import Encoder
from ssd1306 import SSD1306_SPI
from fm_radio import Radio
from machine import Pin, Timer
import utime
from screens import Screen

screen = Screen()
time = [1,3,45,3]
while True: 
    screen.standby(time, [1,5,31,3],0,1, 101.3)
    time[1]+=1
    print(time[1])
    utime.sleep(1)