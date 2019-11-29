import logging
import pwnagotchi.ui.fonts as fonts

from pwnagotchi.ui.hw.base import DisplayImpl

import time
from PIL import Image

class Nokia5110(DisplayImpl):
    def __init__(self, config):
        super(Nokia5110, self).__init__(config, 'nokia5110')
        self._display = None

    def layout(self):
        fonts.setup(8, 8, 8, 12)
        self._layout['width'] = 84
        self._layout['height'] = 48
        self._layout['face'] = (0, 10)
        self._layout['name'] = (0, 30)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (17, 0)
        self._layout['uptime'] = (34, 0)
        self._layout['line1'] = [0, 8, 84, 8]
        self._layout['line2'] = [0, 40, 84, 40]
        self._layout['friend_face'] = (45, 10)
        self._layout['friend_name'] = (45, 30)
        self._layout['shakes'] = (0, 40)
        self._layout['mode'] = (62, 40)
        self._layout['status'] = {
            'pos': (42, 8),
            'font': fonts.Small,
            'max': 10
        }
        return self._layout

    def initialize(self):
        logging.info("initializing 'nokia5110' display")
        self._display = self.nokialcdinit()
        self._display.clear()
        self._display.display()

    def render(self,canvas):
        canvas.save('/home/test.png',format='png')
        canvas.close()
        image = Image.open('/home/test.png').resize((84,48),Image.ANTIALIAS).convert('1')
        self._display.image(image)
        self._display.display()
        image.close()
        self.refresh()

    def clear(self):
        self._display.clear()
        self._display.display()
        self.refresh()

    def refresh(self):
        time.sleep(0.1)

    def nokialcdinit(self):
        DC = 23
        RST = 24
        SPI_PORT = 0
        SPI_DEVICE = 0
        import pwnagotchi.ui.hw.libs.nokia5110.SPI as SPI
        import pwnagotchi.ui.hw.libs.nokia5110.PCD8544 as PCD8544
        self._display = PCD8544.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz = 4000000))
        self._display.begin(contrast=70,bias=4)
        return self._display