from vgamepad import VDS4Gamepad
import time

class GamepadSimulator:
    def __init__(self):
        self.gamepad = VDS4Gamepad()

    def set_input(self, lx, lt, rt):
        """Simulate controller inputs based on the model's prediction.
            We first transform the predicted values into values that 
            the gamepad simulator understands.
            We then prevent the model from gassing and braking at the same time."""
        # Left joystick for steering (LX)
        LX = round(int((lx + 1) * 127), 3)
        # Convert -1,1 to 0,255
        brake_value = round(int(((lt + 1) / 2) * 255), 3)  
        # Convert -1,1 to 0,255
        gas_value = round(int(((rt + 1) / 2) * 255), 3)  

        # Uncomment to print the predicted moves
        # print(f"Predicted LX: {LX}, LT: {brake_value}, RT: {gas_value}")

        priority = max(brake_value, gas_value)

        if priority == brake_value:
             # Left trigger (LT) for brake - Map [-1, 1] to [0, 255]
             self.gamepad.left_trigger(brake_value)
        elif priority == gas_value:
            gas_value = int(gas_value)
            # Right trigger (RT) for gas - Map [-1, 1] to [0, 255]
            self.gamepad.right_trigger(gas_value)

        # LX = max(min(LX, 1), -1)
        self.gamepad.left_joystick(LX, 128) # LX is between -1 and 1
        
        # Update the gamepad state
        self.gamepad.update()
        time.sleep(0.01)

    def set_input_classification(self, lx, lt, rt):
        """Simulate controller inputs based on the model's prediction."""
        # Left joystick for steering (LX)
        self.gamepad.left_joystick(int((lx + 1) * 127), 128)
        
        # Left trigger (LT) for brake
        self.gamepad.left_trigger(int(lt * 255))
        
        # Right trigger (RT) for gas
        self.gamepad.right_trigger(int(rt * 255))
        
        # Update the gamepad state
        self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()

