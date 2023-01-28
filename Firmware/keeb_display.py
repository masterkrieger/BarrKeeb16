import board
import time
import displayio
import adafruit_displayio_ssd1306

from kmk.modules.layers import Layers as _Layers
from kmk.extensions import Extension, InvalidExtensionEnvironment
from kmk.keys import make_key

class DisplayLayers(_Layers):
    last_top_layer = 0
    hues = (4, 20, 69)

    def after_hid_send(keyboard):
        if keyboard.active_layers[0] != self.last_top_layer:
            self.last_top_layer = keyboard.active_layers[0]
            rgb.set_hsv_fill(self.hues[self.last_top_layer], 255, 255)

class DisplayLogo(display)

    # Create the OLED display object
#     display = adafruit_displayio_ssd1306.SSD1306(
#         displayio.I2CDisplay(board.I2C(), device_address=0x3C),
#         width=SCREEN_WIDTH,
#         height=SCREEN_HEIGHT,
#         rotation=180
#     )

    def display_splash_fox(inverted=False):
        # Create a new display group
        group = displayio.Group()
        
        # Create a bitmap from the image file
        bitmap = displayio.OnDiskBitmap('BarrKeeb16_screenlogo.bmp')
        # Create a TileGrid to hold the bitmap
        tilegrid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        # Add the tilegrid to the group
        group.append(tilegrid)

        # Set the group as the display's root
        display.show(group)
        print("Display Logo")

    def display_layer_text(layer):
        displaytext= {0:"Layer 0",1:"Layer 1",2:"Layer 2"}
        return displaytext.get(layer, "no layer")