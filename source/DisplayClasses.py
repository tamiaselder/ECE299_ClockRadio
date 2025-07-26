from machine import Pin, SPI, Timer  # SPI is a class associated with the machine library. 
import utime 

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
import ssd1306 # this is the driver library and the corresponding class
import framebuf  # this is another library for the display. 
import framebuf2 



# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows


# Initialize I/O pins associated with the oled display SPI interface

spi_sck = Pin(14) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
spi_sda = Pin(15) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
spi_res = Pin(11) # res stands for reset; to be connected to a free GPIO pin
spi_dc  = Pin(12) # dc stands for data/command; to be connected to a free GPIO pin
spi_cs  = Pin(13) # chip select; to be connected to the SPI chip select of the Pico 
