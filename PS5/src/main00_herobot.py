# Library imports
from vex import *
SLEEP_MSEC = 20 
CLAW_MAX_TORQUE_PCT = 20
JOYSTICK_DEADBAND = 15
BUTTON_MOTOR_SPEED = 100

# Brain should be defined by default
brainPS5 = Brain()

controller = Controller() 

right_drive_motor = Motor(Ports.PORT6, 1, True)
left_drive_motor = Motor(Ports.PORT5, 1, True)

#motor port function 
rotate_thing = Motor(Ports.PORT4, 1, True) 
arm = Motor(Ports.PORT1, 1, True)

def apply_deadband(value): 
   return 0 if (abs(value) < JOYSTICK_DEADBAND) else value

def spin_drive_motor( 
    moter,  
    controller_axis, 
    rotate_direction,
    forward_block_condition: bool = False, 
    rear_block_condition: bool = False
) -> None: 
    velocity = apply_deadband(controller_axis.position()) 
    velocity = limit_forward_velocity(velocity, forward_block_condition) 
    velocity = limit_backward_velocity(velocity, rear_block_condition) 
    moter.spin(rotate_direction, velocity, PERCENT) 

def limit_forward_velocity(velocity, forward_block_condition: bool):
    return 0 if (velocity > 0 and forward_block_condition) else velocity

def limit_backward_velocity(velocity, rear_block_condition: bool): 
    return 0 if (velocity < 0 and rear_block_condition) else velocity 

def main(): 
    rotate_thing.set_stopping(HOLD)
    arm.set_stopping(HOLD)
    arm.set_max_torque(CLAW_MAX_TORQUE_PCT, PERCENT)

    while True: 
        spin_drive_motor(right_drive_motor, controller.axisD, FORWARD)
        spin_drive_motor(left_drive_motor, controller.axisA, REVERSE)

        right_button_pressed_up = controller.buttonRUp.pressing() 
        left_button_pressed_up = controller.buttonLUp.pressing()
        left_button_position = right_button_pressed_up - left_button_pressed_up
        arm.spin(FORWARD, (left_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        right_button_pressed_down = controller.buttonRDown.pressing() 
        left_button_pressed_down = controller.buttonLDown.pressing()
        right_button_position = right_button_pressed_down - left_button_pressed_down
        rotate_thing.spin(FORWARD, (right_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        sleep(SLEEP_MSEC) 

main() 