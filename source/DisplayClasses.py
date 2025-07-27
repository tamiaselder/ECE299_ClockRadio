from machine import Pin, SPI, Timer  # SPI is a class associated with the machine library. 
import utime 

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
import ssd1306 # this is the driver library and the corresponding class
import framebuf  # this is another library for the display. 
import framebuf2 

from menu import Menu,Screens
from rotary import Encoder
from fm_radio import Radio

volume_encoder = Encoder(18, 17)
selection_encoder = Encoder(27, 26)

select_button = Pin(28, Pin.IN, Pin.PULL_UP)
snooze_button = Pin(16, Pin.IN, Pin.PULL_UP)

radio = Radio(101.9, 2, False)

menu = Menu(radio, volume_encoder, selection_encoder, select_button, snooze_button)


# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows


# Initialize I/O pins associated with the oled display SPI interface

spi_sck = Pin(14) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
spi_sda = Pin(15) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
spi_res = Pin(11) # res stands for reset; to be connected to a free GPIO pin
spi_dc  = Pin(12) # dc stands for data/command; to be connected to a free GPIO pin
spi_cs  = Pin(13) # chip select; to be connected to the SPI chip select of the Pico 


SPI_DEVICE = 1 
oled_spi = SPI( SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )
oled = ssd1306.SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )

while (True):
    menu.update()

    time = menu.get_time()
    day = menu.get_date()

    oled.fill(0)
    hour = time[0]
    if ( hour < 10):
        hour_str = "0" + str(hour)
    else: hour_str = str(hour)

    minute = time[1]
    if ( minute < 10):
        minute_str = "0" + str(minute)
    else: minute_str = str(minute)

    day_str = str(day[1]) + "/" + str(day[2])

    oled.large_text(hour_str +':'+ minute_str, 2, 2, 3)
    oled.text(day_str, 2, 28, 1)

    oled.show()

#    if  menu.get_screen() == Screens.STANDBY:

