import board
import time
import displayio
import adafruit_displayio_ssd1306

displayio.release_displays()

SCREEN_WIDTH = 128 # OLED display width, in pixels
SCREEN_HEIGHT = 64 # OLED display height, in pixels

# Create the OLED display object
display = adafruit_displayio_ssd1306.SSD1306(
    displayio.I2CDisplay(board.I2C(), device_address=0x3C),
    width=SCREEN_WIDTH,
    height=SCREEN_HEIGHT,
    rotation=180
)

def display_splash_fox():
    # Create a new display group
    group = displayio.Group()
    
    # Create a bitmap from the image file
    bitmap = displayio.OnDiskBitmap('BarrKeeb16_screenlogo.bmp')
    
    # Create a palette with 2 colors (black and white)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF

    # Create a TileGrid to hold the bitmap
    color_converter = displayio.ColorConverter()
    tilegrid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Add the tilegrid to the group
    group.append(tilegrid)

    # Set the group as the display's root
    display.show(group)
    #print("Display Logo")

def display_splash_fox_inverted():
    # Create a new display group
    group = displayio.Group()
    
    # Create a bitmap from the image file
    bitmap = displayio.OnDiskBitmap('BarrKeeb16_screenlogo_inverted.bmp')
    
    # Create a palette with 2 colors (black and white)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF

    # Create a TileGrid to hold the bitmap
    color_converter = displayio.ColorConverter()
    tilegrid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Add the tilegrid to the group
    group.append(tilegrid)

    # Set the group as the display's root
    display.show(group)
    #print("Display Logo Inverted")

def display_layer_text(layer):
    displaytext= {0:"Layer 0",1:"Layer 1",2:"Layer 2"}
    return displaytext.get(layer, "no layer")


