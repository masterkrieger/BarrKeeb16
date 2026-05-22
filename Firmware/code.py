######################
#  BarrKeeb16
#  version 1.3
#  18-MAY-2026
#  Author: Jeremy Barr
#
#  Notes:
#  PCF8574 pins 0-3 = rows (outputs, driven LOW to scan)
#  PCF8574 pins 4-7 = cols (inputs, read HIGH/LOW)
#  Diode orientation: COL2ROW
#  MatrixScanner from kmk.scanners.digitalio
#  No pin inversion needed in adafruit_pcf8574.py
######################

#print("Starting")
import time
import board
import displayio
import digitalio

import adafruit_pcf8574  # modded library to work with KMK
import adafruit_displayio_ssd1306

import terminalio
import neopixel

from adafruit_display_text import label
from display_logo import (
    init_display,
    display_splash_fox_inverted,
    display_layer
)

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.layers import Layers as _Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes

######################
# SHARED I2C BUS
######################

i2c = board.I2C()

######################
# DISPLAY INIT
######################

display = init_display(i2c)

######################
# PCF8574 INIT
######################

# After PCF init - confirm I2C is working
pcf = adafruit_pcf8574.PCF8574(i2c, address=0x20)
print("PCF GPIO initial state:", bin(pcf.read_gpio()))

######################
# KEYBOARD SETUP
######################

keyboard = KMKKeyboard()

encoders = EncoderHandler()

tapdance = TapDance()
tapdance.tap_time = 250
macros = Macros()

keyboard.modules = [encoders, tapdance, macros]

######################
# SWITCH MATRIX
######################

keyboard.matrix = MatrixScanner(
    cols=(
        pcf.get_pin(4),
        pcf.get_pin(5),
        pcf.get_pin(6),
        pcf.get_pin(7)
    ),
    rows=(
        pcf.get_pin(0),
        pcf.get_pin(1),
        pcf.get_pin(2),
        pcf.get_pin(3)
    ),
    diode_orientation=DiodeOrientation.COL2ROW,
    pull=digitalio.Pull.UP,
)

# After matrix setup - confirm it initialized
#print("Matrix configured")
#print("GPIO after MatrixScanner init:", bin(pcf.read_gpio()))
#for i in range(8):
#    print("  pin {} = {}".format(i, pcf.read_pin(i)))
#print("Outputs:", keyboard.matrix.outputs)
#print("Inputs:", keyboard.matrix.inputs)

# all 16 keys show as pressed immediately.
# That's the PCF8574 pin state issue
# — the matrix scanner is reading all pins as active before they settle.
# Add this after the matrix scanner setup:
time.sleep(0.5)

######################
# ENCODERS
######################


encoders.pins = (
    (board.A0, board.A1, board.A2, False),
)

######################
# EXTENSIONS
######################

pixels = neopixel.NeoPixel(
    board.A3,
    4,
    brightness=0.5,
    auto_write=False,
    pixel_order=neopixel.GRB
)

rgb_ext = RGB(
    pixel_pin=board.A3,
    pixels=pixels,
    num_pixels=4,
    animation_mode=AnimationModes.RAINBOW,
    animation_speed=1,
    hue_default=0,
    sat_default=255,
    val_default=200   # brightness
)

rgb_ext.enable = True

keyboard.extensions = [
    rgb_ext,
    MediaKeys()
]

######################
# OLED LABELS
######################

LAYER_LABELS = [

    [  # Layer 0
        "LYR", "WTr", "WTb", "RGB",
        "WUp", "Prv", "Nxt", "Ply",
        "WLf", "WRg", "WMn", "WMx",
        "Cpy", "Pst", "DLf", "DRg",
    ],

    [  # Layer 1
        "LYR", "/", "*", "-",
        "7", "8", "9", "+",
        "4", "5", "6", ".",
        "1", "2", "3", "0",
    ],

    [  # Layer 2
        "LYR", "H+", "V+", "A+",
        "S+", "H-", "V-", "A-",
        "Swr", "Kng", "BrR", "S+",
        "Pln", "Brt", "Rnb", "S-",
    ],
]


######################
# CUSTOM LAYERS MODULE
######################

class Layers(_Layers):
    last_top_layer = -1
    hues = (4, 20, 69)

    # In the Layers class - confirm after_hid_send is being called
    def after_hid_send(self, keyboard):
        current = keyboard.active_layers[0]
        if current != self.last_top_layer:
            self.last_top_layer = current
            display_layer(current, LAYER_LABELS[current])


keyboard.modules.append(Layers())

keyboard.debug_enabled = False

######################
# MACROS
######################

WIN_RIGHT = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.RIGHT),
    Release(KC.LGUI),
    Tap(KC.ESC)
)

WIN_LEFT = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.LEFT),
    Release(KC.LGUI),
    Tap(KC.ESC)
)

WIN_UP = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.UP),
    Release(KC.LGUI)
)

WIN_MIN = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.M),
    Release(KC.LGUI)
)

WIN_MAX = KC.MACRO(
    Press(KC.LGUI),
    Press(KC.LSHIFT),
    Tap(KC.M),
    Release(KC.LSHIFT),
    Release(KC.LGUI)
)

DESK_RIGHT = KC.MACRO(
    Press(KC.LGUI),
    Press(KC.LCTRL),
    Tap(KC.RIGHT),
    Release(KC.LCTRL),
    Release(KC.LGUI)
)

DESK_LEFT = KC.MACRO(
    Press(KC.LGUI),
    Press(KC.LCTRL),
    Tap(KC.LEFT),
    Release(KC.LCTRL),
    Release(KC.LGUI)
)

WIN_TAB = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.TAB),
    Release(KC.LGUI)
)

COPY = KC.LCTRL(KC.C)

PASTE = KC.LCTRL(KC.V)

POWERSHELL = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.R),
    Release(KC.LGUI),
    Tap(KC.P),
    Tap(KC.O),
    Tap(KC.W),
    Tap(KC.E),
    Tap(KC.R),
    Tap(KC.S),
    Tap(KC.H),
    Tap(KC.E),
    Tap(KC.L),
    Tap(KC.L),
    Tap(KC.ENTER)
)

WIN_TERMINAL = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.R),
    Release(KC.LGUI),
    Tap(KC.W),
    Tap(KC.T),
    Tap(KC.ENTER)
)

QUAKE = KC.LGUI(KC.ESC)

_______ = KC.TRNS
xxxxxxx = KC.NO

######################
# TAP DANCE
######################

TD_LYRS_0 = KC.TD(
    
    KC.KP_ENTER,
    KC.TO(1),
    KC.TO(2),
    KC.TO(0)
)

RGB_LYRS = KC.TD(
    KC.RGB_MODE_PLAIN,
    KC.RGB_MODE_SWIRL,
    KC.RGB_MODE_KNIGHT,
    KC.RGB_MODE_RAINBOW,
    KC.RGB_MODE_BREATHE_RAINBOW
)

# KEYMAPS
keyboard.keymap = [
    [  # Layer 0: WIN MACROS
        TD_LYRS_0, WIN_TERMINAL, WIN_TAB,    RGB_LYRS,
        WIN_UP,    KC.MPRV,      KC.MNXT,    KC.MPLY,
        WIN_LEFT,  WIN_RIGHT,    WIN_MIN,    WIN_MAX,
        COPY,      PASTE,        DESK_LEFT,  DESK_RIGHT ,
    ],
    [  # Layer 1: NUMPAD
        TD_LYRS_0,   KC.KP_SLASH,   KC.KP_ASTERISK,   KC.KP_MINUS,
        KC.P7,       KC.P8,         KC.P9,            KC.KP_PLUS,
        KC.P4,       KC.P5,         KC.P6,            KC.PDOT,
        KC.P1,       KC.P2,         KC.P3,            KC.P0,
    ],
    [  # Layer 2: RGB CTL
        TD_LYRS_0,          KC.RGB_HUI,          KC.RGB_VAI,                   KC.RGB_ANI,
        KC.RGB_SAI,         KC.RGB_HUD,          KC.RGB_VAD,                   KC.RGB_AND,    
        KC.RGB_MODE_SWIRL,  KC.RGB_MODE_KNIGHT,  KC.RGB_MODE_BREATHE_RAINBOW,  KC.RGB_SAI,
        KC.RGB_MODE_PLAIN,  KC.RGB_MODE_BREATHE, KC.RGB_MODE_RAINBOW,          KC.RGB_SAD,    
    ],
]

######################
# ENCODER MAPS
######################

encoders.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),),
    ((KC.VOLD, KC.VOLU, KC.MUTE),),
    ((KC.RGB_AND, KC.RGB_ANI, KC.RGB_TOG),),
]

######################
# BOOT DISPLAY
######################


display_splash_fox_inverted()
time.sleep(1)


display_layer(
    0,
    LAYER_LABELS[0]
)

keyboard.debug_enabled = False

######################
# START
######################

if __name__ == '__main__':
    # DEBUG: manually simulate one scan cycle
    #import time
    #print("Simulating scan...")
    #pcf.write_gpio(0xFF)  # all HIGH
    #time.sleep(0.01)

    #for row_pin in range(4):
    #    pcf.write_pin(row_pin, False)  # drive row LOW
    #    time.sleep(0.01)
    #    gpio = pcf.read_gpio()
    #    print("Row {} LOW, GPIO={}".format(row_pin, bin(gpio)))
    #    for col_pin in range(4, 8):
    #        print("  Col {} = {}".format(col_pin, pcf.read_pin(col_pin)))
    #    pcf.write_pin(row_pin, True)
    #    time.sleep(0.01)

    #print("Hold a key and check output above")
    keyboard.go()