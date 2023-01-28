######################
#  BarrKeeb16
#  version 1.0
#  28-Dec-2022
#  Author: Jeremy Barr
#
#  Notes:
#  kmk.matrix modified for PCF8574 output LOW when polling columns.
#  PCF8574 modified to read pin value as opposite value. KMK reads pin HIGH as keypress, but that's default input value.
######################

#print("Starting")

import board
import displayio

import adafruit_pcf8574  # modded library to work with KMK
import adafruit_displayio_ssd1306

import terminalio
import neopixel
from adafruit_display_text import label
from display_logo import display_splash_fox_inverted

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.layers import Layers as _Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB

# init IO Expander
pcf = adafruit_pcf8574.PCF8574(board.I2C(), address=0x20)

# KEYBOARD SETUP
#layers = Layers()
keyboard = KMKKeyboard()
encoders = EncoderHandler()
tapdance = TapDance()
tapdance.tap_time = 250
keyboard.modules = [encoders, tapdance]

# SWITCH MATRIX
keyboard.col_pins = (pcf.get_pin(4), pcf.get_pin(5), pcf.get_pin(6), pcf.get_pin(7))
keyboard.row_pins = (pcf.get_pin(0), pcf.get_pin(1), pcf.get_pin(2), pcf.get_pin(3))
keyboard.diode_orientation = DiodeOrientation.ROWS

# ENCODERS
encoders.pins = ((board.A0, board.A1, board.A2, False),)

# EXTENSIONS
rgb_ext = RGB(pixel_pin = board.D3, num_pixels=4)#, hue_default=100)
keyboard.extensions = [rgb_ext, MediaKeys()]

# custom functions
class Layers(_Layers):
    last_top_layer = 0
    hues = (4, 20, 69)
    
    def after_hid_send(keyboard):
        print(keyboard.active_layers[0])
        if keyboard.active_layers[0] != self.last_top_layer:
            self.last_top_layer = keyboard.active_layers[0]
            rgb.set_hsv_fill(self.hues[self.last_top_layer], 255, 255)
            display_layer_text(keyboard.active_layers[0])
            #print(keyboard.active_layers[0])
            
keyboard.modules.append(Layers())

keyboard.debug_enabled = False

# MACROS Layer 1
WIN_RIGHT = simple_key_sequence([KC.LGUI(KC.RIGHT), KC.MACRO_SLEEP_MS(100), KC.ESC])
WIN_LEFT = simple_key_sequence([KC.LGUI(KC.LEFT), KC.MACRO_SLEEP_MS(100), KC.ESC])
WIN_UP = simple_key_sequence([KC.LGUI(KC.UP)])
WIN_MIN = simple_key_sequence([KC.LGUI(KC.M)])
WIN_MAX = simple_key_sequence([KC.LGUI(KC.LSFT(KC.M))])
DESK_RIGHT = simple_key_sequence([KC.LCMD(KC.LCTRL(KC.RIGHT))])
DESK_LEFT = simple_key_sequence([KC.LCMD(KC.LCTRL(KC.LEFT))])
WIN_TAB = simple_key_sequence([KC.LCMD(KC.TAB)])
COPY = KC.LCTRL(KC.C)
PASTE = KC.LCTRL(KC.V)
POWERSHELL = simple_key_sequence([KC.LCMD(KC.R), KC.MACRO_SLEEP_MS(250), send_string('powershell'), KC.ENTER])

# NEOPIXEL RGB
#RGB_COLORS = KC.TD(Color.RED, Color.GREEN, Color.BLUE, Color.WHITE, Color.YELLOW, Color.ORANGE)
#TODO: change to NEOPIXEL functions
# Color_RED = rgb_ext.set_hsv_fill(0,100,100)
# Color_BLUE = rgb_ext.set_hsv_fill(240,100,100)
# Color_MAGENTA = rgb_ext.set_hsv_fill(300,100,100)
# Color_ORANGE = rgb_ext.set_hsv_fill(30,100,100)
# Color_WHITE = rgb_ext.set_hsv_fill(0,0,100)
# Color_GREEN = rgb_ext.set_hsv_fill(120,100,100)

_______ = KC.TRNS
xxxxxxx = KC.NO

# LAYER SWITCHING TAP DANCE
#TD_LYRS_1 = KC.TD(KC.KP_ENTER, KC.TO(1), KC.TO(2), KC.TO(0))
TD_LYRS_0 = KC.TD(KC.KP_ENTER, KC.TO(0))
TD_LYRS_1 = KC.TD(KC.KP_ENTER, KC.TO(1))
TD_LYRS_2 = KC.TD(KC.KP_ENTER, KC.TO(2))
RGB_LYRS = KC.TD(KC.RGB_MODE_PLAIN, KC.RGB_MODE_SWIRL, KC.RGB_MODE_KNIGHT, KC.RGB_MODE_RAINBOW, KC.RGB_MODE_BREATHE_RAINBOW)

# KEYMAPS
keyboard.keymap = [
    [  # Layer 0: WIN MACROS
        TD_LYRS_1, POWERSHELL,   WIN_TAB,    RGB_LYRS,
        WIN_UP,    KC.MPRV,      KC.MNXT,    KC.MPLY,
        WIN_LEFT,  WIN_RIGHT,    WIN_MIN,    WIN_MAX,
        COPY,      PASTE,        DESK_LEFT,  DESK_RIGHT ,
    ],
    [  # Layer 1: NUMPAD
        TD_LYRS_2,   KC.KP_SLASH,   KC.KP_ASTERISK,   KC.KP_MINUS,
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

encoders.map = [    ((KC.VOLD, KC.VOLU, KC.MUTE),),   # MEDIA
                    ((KC.VOLD, KC.VOLU, KC.MUTE),),   # MEDIA
                    ((KC.RGB_AND, KC.RGB_ANI, KC.RGB_TOG),),   # RGB
                ]

#print("Keyboard Go!")
display_splash_fox_inverted()
if __name__ == '__main__':
    keyboard.go()