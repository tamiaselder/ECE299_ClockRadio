from machine import I2C, Pin
from micropython import const

class RDA5807M():
    def __init__(self, i2c: I2C) -> None:
        self.i2c = i2c
        self.channel = 0
        self.volume = 0
        self.__chip_id = 0x10
        self.__w_buf = bytearray(2)
        self.__r_buf = bytearray(2)
    
    def radio_init(self):
        #self.__w_buf = [0b11100111, 0b11011001]
        self.__w_buf[0] = 0b11100111
        self.__w_buf[1] = 0b11011001
        print(self.__w_buf)
        self.write_reg(0x02)
        print(self.i2c.readfrom_mem(0x10,0x02,2))
        self.read_reg(0x02)
        result = int(self.__r_buf[0]) << 8 + self.__r_buf[1]
        self.channel = (result & 0xff80) >> 9
        print(self.channel*0.1 + 87)
    
    def write_reg(self, addr):
        self.i2c.writeto_mem(self.__chip_id, addr, self.__w_buf)
    
    def read_reg(self, addr):
        self.i2c.readfrom_mem_into(self.__chip_id, addr, self.__r_buf)
        

radio_sck = Pin(17)
radio_sda = Pin(16)
radio = I2C(0, scl=radio_sck, sda=radio_sda, freq=400000)
rd = RDA5807M(radio)

rd.radio_init()