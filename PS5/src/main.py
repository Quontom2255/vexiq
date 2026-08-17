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

brainPS5.screen.print("FBI") 

from vex import * 

JOYSTICK_DEADBAND = 15
BUTTON_MOTOR_SPEED = 100
LOOP_SLEEP_MSEC = 20
CLAW_MAX_TORQUE_PCT = 20

m_brain = Brain() 
right_drive_motor = Motor(Ports.PORT6)
left_drive_motor = Motor(Ports.PORT1)
controller = Controller() 
claw = Motor(Ports.PORT4) 
arm = Motor(Ports.PORT10)

def apply_deadband(value): 
    if abs(value)<JOYSTICK_DEADBAND: 
        return 0 
    else: 
        return value

def main(): 
    claw.set_stopping(HOLD)
    arm.set_stopping(HOLD)
    arm.set_max_torque(CLAW_MAX_TORQUE_PCT, PERCENT)

    while True: 
        right_velocity = apply_deadband(controller.axisD.position()) 
        left_velocity = apply_deadband(controller.axisA.position()) 
        right_drive_motor.spin(REVERSE, right_velocity, PERCENT)
        left_drive_motor.spin(FORWARD, left_velocity, PERCENT) 

        right_button_pressed_down = controller.buttonRUp.pressing() 
        left_button_pressed_down = controller.buttonLUp.pressing()
        right_button_position = right_button_pressed_down - left_button_pressed_down
        claw.spin(FORWARD, (right_button_position) * BUTTON_MOTOR_SPEED, PERCENT) 

        right_button_pressed_up = controller.buttonRDown.pressing() 
        left_button_pressed_up = controller.buttonLDown.pressing()
        left_button_position = left_button_pressed_up - right_button_pressed_up
        arm.spin(FORWARD, (left_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        sleep(LOOP_SLEEP_MSEC)

main() 