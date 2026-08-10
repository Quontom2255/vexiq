# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       영재정보교육                                                       #
# 	Created:      7/27/2026, 2:13:33 PM                                        #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brainPS5=Brain()

brainPS5.screen.print("Quontom2255") 

from vex import * 

m_brain = Brain() 
right_drive_motor = Motor(Ports.PORT6)
left_drive_motor = Motor(Ports.PORT1)
controller = Controller() 
claw = Motor(Ports.PORT4) 

def main(): 
    while True: 
        right_velocity = controller.axisD.position() 
        left_velocity = controller.axisA.position() 
        right_drive_motor.spin(REVERSE, right_velocity, PERCENT)
        left_drive_motor.spin(FORWARD, left_velocity, PERCENT) 
        right_button_pressed_down = controller.buttonRDown.pressing() 
        right_button_pressed_up = controller.buttonRUp.pressing()
        right_button_position = right_button_pressed_up - right_button_pressed_down
        claw.spin(FORWARD, (controller.buttonRDown.pressing() - controller.buttonLDown.pressing()) * 100, PERCENT) 
main() 