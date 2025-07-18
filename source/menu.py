from fm_radio import Radio
from datetime import datetime as dt
from enum import Enum

class clockSettings(Enum):
    TIME = 0
    TIME_FORTMAT = 1
    ALARM_TIME = 2

class Menu():
    def __init__(self, radio: Radio):
        self.radio = radio

        self.menu_options = [
            'Radio',
            'Clock',
        ]

        self.clock_setting = [
            '',
            'Time',
        ]

        self.current_option = 0
        