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
    # screen.standby(time, 1, [1,5,31,3],7,35,False, 101.3)
    # utime.sleep(10)
    screen.time_menu(time,[1,5,31,3],1 , 10, 25, 0)
    screen.hlt_alrmst()
    screen.hlt_alrm()
    screen.hlt_clkmd()
    screen.hlt_time()
    time[1]+=1
    time[0]+=1
    utime.sleep(10)