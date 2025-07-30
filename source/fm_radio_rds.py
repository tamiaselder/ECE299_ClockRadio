from machine import Pin, I2C 
import utime

class Radio:
    
    def __init__( self, NewFrequency, NewVolume, NewMute ):

#
# set the initial values of the radio
#
        self.Volume = 3
        self.Frequency = 88
        self.Mute = False
#
# Update the values with the ones passed in the initialization code
#
        self.SetVolume( NewVolume )
        self.SetFrequency( NewFrequency )
        self.SetMute( NewMute )
      
# Initialize I/O pins associated with the radio's I2C interface

        self.i2c_sda = Pin(8)
        self.i2c_scl = Pin(9)


        self.i2c_device = 0
        self.i2c_device_address = 0x10

#
# Array used to configure the radio
#
        self.Settings = bytearray( 8 )
        self.RDS = bytearray( 12 )

        self.radio_i2c = I2C( self.i2c_device, scl=self.i2c_scl, sda=self.i2c_sda, freq=400000)
        self.ProgramRadio()
        self.clear_rds_data()

    def SetVolume( self, NewVolume ):
#
# Conver t the string into a integer
#
        # try:
        #     NewVolume = int( NewVolume )
            
        # except:
        #     return( False )
        
#
# Validate the type and range check the volume
#
        # if ( not isinstance( NewVolume, int )):
        #     return( False )
        
        # if (( NewVolume < 0 ) or ( NewVolume > 15 )):
        #     return( False )

        self.Volume = NewVolume
        return( True )



    def SetFrequency( self, NewFrequency ):
#
# Convert the string into a floating point value
#
        try:
            NewFrequency = float( NewFrequency )
            
        except:
            return( False )
#
# validate the type and range check the frequency
#
        if ( not ( isinstance( NewFrequency, float ))):
            return( False )
 
        if (( NewFrequency < 88.0 ) or ( NewFrequency > 108.0 )):
            return( False )

        self.Frequency = NewFrequency
        return( True )
        
    def SetMute( self, NewMute ):
        
        # try:
        #     self.Mute = bool( int( NewMute ))
            
        # except:
        #     return( False )
        
        return( True )

    def clear_rds_data(self):

        """ Clear RDS data, e.g. after retuning """

        self.last_ab = 0
        self.station_name = [" " for i in range(8)]
        self.station_name_buffer = [" " for i in range(8)]
        self.radio_text = [" " for i in range(64)]
        self.radio_text_buffer = [" " for i in range(64)]
        self.last_offset = 0
        self.last_st_offset = 0
        self.hours = 0
        self.minutes = 0
#
# convert the frequency to 10 bit value for the radio chip
#
    def ComputeChannelSetting( self, Frequency ):
        Frequency = int( Frequency * 10 ) - 870
        
        ByteCode = bytearray( 2 )
#
# split the 10 bits into 2 bytes
#
        ByteCode[0] = ( Frequency >> 2 ) & 0xFF
        ByteCode[1] = (( Frequency & 0x03 ) << 6 ) & 0xC0
        return( ByteCode )

#
# Configure the settings array with the mute, frequency and volume settings
#
    def UpdateSettings( self ):
        
        self.Settings = bytearray (8)
        
        if ( self.Mute ):
            self.Settings[0] = 0x80
        else:
            self.Settings[0] = 0xC0
  
        self.Settings[1] = 0x09 | 0x04
        self.Settings[2:3] = self.ComputeChannelSetting( self.Frequency )
        self.Settings[3] = self.Settings[3] | 0x10
        self.Settings[4] = 0x04
        self.Settings[5] = 0x00
        self.Settings[6] = 0x84
        self.Settings[7] = 0x80 + self.Volume

#        
# Update the settings array and transmitt it to the radio
#
    def ProgramRadio( self ):

        self.UpdateSettings()
        self.radio_i2c.writeto( self.i2c_device_address, self.Settings )


#
# Extract the settings from the radio registers
#
    def GetSettings( self ):
#        
# Need to read the entire register space. This is allow access to the mute and volume settings
# After and address of 255 the 
#
        self.RadioStatus = self.radio_i2c.readfrom( self.i2c_device_address, 256 )

        if (( self.RadioStatus[0xF0] & 0x40 ) != 0x00 ):
            MuteStatus = False
        else:
            MuteStatus = True
            
        VolumeStatus = self.RadioStatus[0xF7] & 0x0F
 
 #
 # Convert the frequency 10 bit count into actual frequency in Mhz
 #
        FrequencyStatus = (( self.RadioStatus[0x00] & 0x03 ) << 8 ) | ( self.RadioStatus[0x01] & 0xFF )
        FrequencyStatus = ( FrequencyStatus * 0.1 ) + 87.0
        
        if (( self.RadioStatus[0x00] & 0x04 ) != 0x00 ):
            StereoStatus = True
        else:
            StereoStatus = False
        
        return( MuteStatus, VolumeStatus, FrequencyStatus, StereoStatus )
    
    def GetRDS(self):
        self.RDS = self.radio_i2c.readfrom( self.i2c_device_address, 12)
        
        status = self.RDS[0x01]
        if(status & 0x80 != 0x00):
            a = self.RDS[0x04] & 0xFF << 8 | self.RDS[0x05]
            b = self.RDS[0x06] & 0xFF << 8 | self.RDS[0x07]
            c = self.RDS[0x08] & 0xFF << 8 | self.RDS[0x09]
            d = self.RDS[0x0A] & 0xFF << 8 | self.RDS[0x0B]

            program_information = a
            group_type = b >> 12
            group_version = (b >> 11) & 1
            traffic_program = (b >> 10) & 1
            program_type = (b >> 5) & 0x1f
            
            #station name
            if group_type == 0:
                offset = b & 0x3
                character_a = chr(d >> 8)
                character_b = chr(d & 0xff)
                
                # print(character_a)
                # print(character_b)
                #Check multiple messages for consistency          
                self.station_name_buffer[offset*2] = character_a
                self.station_name_buffer[(offset*2)+1] = character_b
                if offset < self.last_st_offset:
                    self.station_name = self.station_name_buffer
                    print(self.station_name)
                self.last_st_offset = offset
                            
            #radio text   
            elif group_type == 2 and group_version == 0:
                offset = b & 0xf
                
                ab = (b >> 4) & 1
                character_a = c >> 8
                character_b = c & 0xff
                character_c = d >> 8
                character_d = d & 0xff
                if ab != self.last_ab:
                    self.clear_buffer = True
                    self.radio_text_buffer = [" " for i in range(64)]
                self.last_ab = ab
                self.radio_text_buffer[offset*4] = chr(character_a)
                self.radio_text_buffer[(offset*4)+1] = chr(character_b)
                self.radio_text_buffer[(offset*4)+2] = chr(character_c)
                self.radio_text_buffer[(offset*4)+3] = chr(character_d)

                if offset < self.last_offset:
                    self.radio_text = self.radio_text_buffer
                self.last_offset = offse
        
            #radio text type 2
            elif group_type == 2 and group_version == 1:
                offset = b & 0xf
                ab = (b >> 4) & 1
                character_c = d >> 8
                character_d = d & 0xff
                if ab != self.last_ab:
                    self.radio_text_buffer = [" " for i in range(64)]
                self.radio_text_buffer[(offset*2)+0] = chr(character_c)
                self.radio_text_buffer[(offset*2)+1] = chr(character_d)
                
                # print(chr(character_c))
                # print(chr(character_d))

                if offset < self.last_offset:
                    self.radio_text = self.radio_text_buffer
                    print(self.radio_text)
                self.last_offset = offset


    
# radio = Radio(100.3, 2, False)

# while True:
#     radio.GetRDS()
#     utime.sleep_ms(100)