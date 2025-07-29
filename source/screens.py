from machine import Pin, SPI  # SPI is a class associated with the machine library. 
import ssd1306 # this is the driver library and the corresponding class
import framebuf  # this is another library for the display. 
import framebuf2 


class Screen():
    def __init__(self):
        # Define columns and rows of the oled display. These numbers are the standard values. 
        SCREEN_WIDTH = 128 #number of columns
        SCREEN_HEIGHT = 64 #number of rows


        # Initialize I/O pins associated with the oled display SPI interface
        spi_sck = Pin(14) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
        spi_sda = Pin(15) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
        spi_res = Pin(11) # res stands for reset; to be connected to a free GPIO pin
        spi_dc  = Pin(12) # dc stands for data/command; to be connected to a free GPIO pin
        spi_cs  = Pin(13) # chip select; to be connected to the SPI chip select of the Pico 

        SPI_DEVICE = 1 # Because the peripheral is connected to SPI 0 hardware lines of the Pico

        # initialize the SPI interface for the OLED display
        oled_spi = SPI(SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )

        # Initialize the display
        self.oled = ssd1306.SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )
    
    def clear_disp(self):
        self.oled.fill(0)
        self.oled.show()

    def standby(self, time, time_frmt, day, alrm_hr, alrm_min, alrm_set, radio_st):

        hour = time[0]
        if (hour < 10 and time_frmt): # 24 hour mode == 1
            hour_str = "0" + str(hour)
        elif (hour < 10 and not time_frmt):
            hour_str = " " + str(hour)
        else: hour_str = str(hour)

        minute = time[1]
        if ( minute < 10):
            minute_str = "0" + str(minute)
        else: minute_str = str(minute)

        day_names = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        day_str = day_names[day[3]-1] + " " + month_names[day[1]-1] + " " + str(day[2])

        radio_str = str(radio_st) + " Rock Music"
        
        alrm_state = ["Off","On "]
        alrm_str = "Alarm " + alrm_state[alrm_set] + " " + str(alrm_hr) + ":" + str(alrm_min)
        
        #self.oled.contrast(250)
        self.oled.fill(0)
        self.oled.large_text(hour_str +':'+ minute_str, 4, 4, 3)
        self.oled.text(day_str, 0, 32, 1)
        self.oled.text(radio_str, 0, 43, 1)
        self.oled.text(alrm_str, 0, 54, 1)
        self.oled.show()


    def time_menu(self, time, day, alrm_st, alrm_hr, alrm_min, time_frmt):
        
        hour = time[0]
        if (hour < 10 and time_frmt): # 24 hour mode == 1
            hour_str = "0" + str(hour)
        elif (hour < 10 and not time_frmt):
            hour_str = " " + str(hour)
        else: hour_str = str(hour)

        minute = time[1]
        if ( minute < 10):
            minute_str = "0" + str(minute)
        else: minute_str = str(minute)


        if (alrm_hr < 10 and time_frmt): # 24 hour mode == 1
            alrm_hour_str = "0" + str(alrm_hr)
        elif (alrm_hr < 10 and not time_frmt):
            alrm_hour_str = " " + str(alrm_hr)
        else: alrm_hour_str = str(alrm_hr)

        if (alrm_min < 10):
            alrm_minute_str = "0" + str(alrm_min)
        else: alrm_minute_str = str(alrm_min)

        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        DayOfWeek = day_names[day[3]-1]

        date = str(day[2])
        month = str(day[1])
        year = str(day[0])

        time_type = ["12h", "24h"]
        alrm_state = ["Alarm is On", "Alarm is Off"]

        #display output
        self.oled.fill(0)
        self.oled.text("Clock Settings", 8, 0, 1)
        self.oled.text("Time:", 0, 14, 1)
        self.oled.large_text(hour_str +':'+ minute_str, 47, 10, 2)
        self.oled.text("Clock Mode: " + time_type[time_frmt], 0, 28, 1)
        self.oled.text("Alarm:", 0, 42, 1)
        self.oled.large_text(alrm_hour_str + ":" + alrm_minute_str, 47, 38, 2)
        self.oled.text(alrm_state[alrm_st], 0, 56, 1)
        self.oled.show()
    

    def hlt_time_hr(self):
        self.oled.rect(47, 8, 33, 18, 1)
        self.oled.show()

    def hlt_time_min(self):
        self.oled.rect(95, 8, 33, 18, 1)
        self.oled.show()

    def hlt_clkmd(self):
        self.oled.rect(95, 26, 33, 11, 1)
        self.oled.show()

    def hlt_alrm_hr(self):
        self.oled.rect(47, 36, 33, 18, 1)
        self.oled.show()

    def hlt_alrm_min(self):
        self.oled.rect(95, 36, 33, 18, 1)
        self.oled.show()

    def hlt_alrmst(self):
        self.oled.rect(70, 54, 28, 10, 1)
        self.oled.show()

    def radio_menu(self, radio_st, rds_info, volume):
        #display output
        self.oled.fill(0)
        self.oled.text("Radio Info", 24, 0, 1)
        self.oled.large_text(str(round(radio_st, 1)) + " FM", 0, 12, 2)
        self.oled.text(rds_info, 0, 30, 1)
        self.oled.text("Volume " + str(volume), 0, 40, 1)
        self.oled.show()

    def face(self):
        self.oled.fill(0)
        self.oled.large_text("oo", 0, 0, 8)
        self.oled.show()
