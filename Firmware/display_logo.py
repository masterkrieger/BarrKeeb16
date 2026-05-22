import board
import displayio
import i2cdisplaybus
import adafruit_displayio_ssd1306

import terminalio

from adafruit_display_text import label

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

display = None


def init_display(i2c):

    global display

    try:
        displayio.release_displays()
    except:
        pass

    display_bus = i2cdisplaybus.I2CDisplayBus(
        i2c,
        device_address=0x3C
    )

    display = adafruit_displayio_ssd1306.SSD1306(
        display_bus,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        rotation=180
    )

    return display


def display_splash_fox_inverted():

    group = displayio.Group()

    bitmap = displayio.OnDiskBitmap(
        'BarrKeeb16_screenlogo_inverted.bmp'
    )

    tilegrid = displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader
    )

    group.append(tilegrid)

    display.root_group = group


def display_splash_fox():

    group = displayio.Group()

    bitmap = displayio.OnDiskBitmap(
        'BarrKeeb16_screenlogo.bmp'
    )

    tilegrid = displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader
    )

    group.append(tilegrid)

    display.root_group = group


def display_layer(layer_index, keymap):
    display.root_group = displayio.Group()  # clear screen
    
    layer_names = {
        0: "WIN",
        1: "NUM",
        2: "RGB"
    }

    encoder_modes = {
        0: "VOL",
        1: "VOL",
        2: "RGB"
    }

    group = displayio.Group()

    ######################
    # HEADER
    ######################

    header = label.Label(
        terminalio.FONT,
        text="L{} {} ENC:{}".format(
            layer_index,
            layer_names.get(layer_index, "?"),
            encoder_modes.get(layer_index, "?")
        ),
        color=0xFFFFFF,
        x=0,
        y=6
    )

    group.append(header)

    ######################
    # KEY GRID
    ######################

    for row in range(4):

        row_text = ""

        for col in range(4):

            idx = row * 4 + col

            key = str(keymap[idx])[:3]

            row_text += "{:<4}".format(key)

        lbl = label.Label(
            terminalio.FONT,
            text=row_text,
            color=0xFFFFFF,
            x=0,
            y=18 + (row * 11)
        )

        group.append(lbl)

    display.root_group = group