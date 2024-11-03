import vgamepad as vg
import time

gamepad = vg.VDS4Gamepad()

time.sleep(10)
print('pressting RT')
gamepad.right_trigger(255)
gamepad.left_joystick(255, 128)
# gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
gamepad.update()

time.sleep(4)

print('releasign RT and pressing LT')
gamepad.right_trigger(0)
gamepad.left_trigger(255)
gamepad.left_joystick(0, 128)
gamepad.update()

time.sleep(4)