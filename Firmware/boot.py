import storage
import board
import digitalio

switch = digitalio.DigitalInOut(board.A2)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
print(switch.value)

# Normal operation: USB drive hidden, switch.value is True (A2 floating/pulled up)
# For editing: ground A2 pin to expose USB drive to PC
# TODO: uncomment storage.disable_usb_drive() when done editing
if switch.value:
    storage.disable_usb_drive()
else:
    pass # editing mode, USB drive stays visible
    