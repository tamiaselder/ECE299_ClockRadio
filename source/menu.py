from fm_radio import Radio
from datetime import datetime as dt

class Menu():
    def __init__(self, radio: Radio):
        self.radio = radio

        self.menu_options = [
            'Radio',
            'Clock',
            'Alarm',
            'Settings'
        ]

        self.setting_options = [
            'Alarm Volume',
            'Snooze Time',
        ]

        self.current_option = 0
        