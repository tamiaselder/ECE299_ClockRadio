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

button = Pin(15, Pin.IN, Pin.PULL_DOWN)
pressed = True

#
# SPI Device ID can be 0 or 1. It must match the wiring. 
#
SPI_DEVICE = 1 # Because the peripheral is connected to SPI 0 hardware lines of the Pico

#
# initialize the SPI interface for the OLED display
#
oled_spi = SPI( SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )

#
# Initialize the display
#
oled = ssd1306.SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )

# tim = Timer(1)

# # Assign a value to a variable
#Count = 3113

# def tim_callback(x):
#         global Count
#         if(button.value() == 1):
#                 Count += 1

# def button_callback(x):
#         tim.init(mode=Timer.ONE_SHOT, period=10, callback =tim_callback)


# button.irq(button_callback, Pin.IRQ_RISING)

while ( True ):
        
        

  
#
# Clear the buffer
#
        oled.fill(0)
        
#
# Update the text on the screen
#
        # oled.text("Welcome to ECE", 0, 0, 1) # Print the text starting from 0th column and 0th row
        # oled.text("299", 45, 10, 0) # Print the number 299 starting at 45th column and 10th row
        # oled.text("Count is: %4d" % Count, 0, 30, 0) # Print the value stored in the variable Count. 
        
#
# Draw box below the text
#
        #led.rect( 64, 0, 64, 32, 0, True )        
        #oled.rect( 0, 0, 128, 32, 1 ) 
        #oled.text("Welcome to ECE", 0, 2, 1) # Print the text starting from 0th column and 0th row
        oled.large_text(str(sample_time)+':'+str(sample_time), 2, 2, 3)

#
# Transfer the buffer to the screen
#
        oled.show()

        sample_time += 1
        utime.sleep(1)