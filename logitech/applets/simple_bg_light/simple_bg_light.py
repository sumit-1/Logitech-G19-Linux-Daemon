from logitech.g19_keys import (Data, Key)
from logitech.g19_receivers import InputProcessor
from logitech.g19_config import G19Config


class light(object):
    '''Simple color changing.

    Enable M1..3 for red/green/blue and use the scroll to change the intensity
    for the currently selected colors.

    '''

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__redEnabled = False
        self.__greenEnabled = False
        self.__blueEnabled = False
        self.__bgconf = G19Config("simple_bg_light")
        self.__curColor = [self.__bgconf.read("red", "255", "int"), self.__bgconf.read("green", "255", "int"), self.__bgconf.read("blue", "255", "int")]
        self.__lg19.load_text("    simple_bg_light", 1, True)
        self.__lg19.load_text("Red:   "+str(self.__curColor[0]), 3)
        self.__lg19.load_text("Green: "+str(self.__curColor[1]), 4)
        self.__lg19.load_text("Blue:  "+str(self.__curColor[2]), 5)
        self.__lg19.load_text("Press SETTINGS to save", 7)
        self.__lg19.set_text()
        self.__lg19.set_bg_color(*self.__curColor)


    def _clamp_current_color(self):
        '''Assures that all color components are in [0, 255].'''
        for i in range(3):
            val = self.__curColor[i]
            self.__curColor[i] = val if val >= 0 else 0
            val = self.__curColor[i]
            self.__curColor[i] = val if val <= 255 else 255

    def stop(self):
        pass
        
    def _update_leds(self):
        '''Updates M-leds according to enabled state.'''
        val = 0
        if self.__redEnabled:
            val |= Data.LIGHT_KEY_M1
        if self.__greenEnabled:
            val |= Data.LIGHT_KEY_M2
        if self.__blueEnabled:
            val |= Data.LIGHT_KEY_M3
        self.__lg19.set_enabled_m_keys(val)

    def get_input_processor(self):
        return self

    def process_input(self, evt):
        processed = False
        
        if Key.SETTINGS in evt.keysDown:
            self.__bgconf.write("red", self.__curColor[0])
            self.__bgconf.write("green", self.__curColor[1])
            self.__bgconf.write("blue", self.__curColor[2])
            
            processed = True
        if Key.M1 in evt.keysDown:
            self.__redEnabled = not self.__redEnabled
            self._update_leds()
            processed = True
        if Key.M2 in evt.keysDown:
            self.__greenEnabled = not self.__greenEnabled
            self._update_leds()
            processed = True
        if Key.M3 in evt.keysDown:
            self.__blueEnabled = not self.__blueEnabled
            self._update_leds()
            processed = True

        oldColor = list(self.__curColor)
        diffVal = 0
        scrollUsed = False

        if Key.SCROLL_UP in evt.keysDown:
            diffVal = 10
            scrollUsed = True
        if Key.SCROLL_DOWN in evt.keysDown:
            diffVal = -10
            scrollUsed = True
        

        atLeastOneColorIsEnabled = False

        if self.__redEnabled:
            self.__curColor[0] += diffVal
            self.__lg19.load_text("Red:   "+str(self.__curColor[0]), 3)
            self.__lg19.set_text()
            atLeastOneColorIsEnabled = True
        if self.__greenEnabled:
            self.__curColor[1] += diffVal
            self.__lg19.load_text("Green: "+str(self.__curColor[1]), 4)
            self.__lg19.set_text()
            atLeastOneColorIsEnabled = True
        if self.__blueEnabled:
            self.__curColor[2] += diffVal
            self.__lg19.load_text("Blue:  "+str(self.__curColor[2]), 5)
            self.__lg19.set_text()
            atLeastOneColorIsEnabled = True

        self._clamp_current_color()
        processed = processed or atLeastOneColorIsEnabled and scrollUsed

        if oldColor != self.__curColor:
            self.__lg19.set_bg_color(*self.__curColor)
        return processed
