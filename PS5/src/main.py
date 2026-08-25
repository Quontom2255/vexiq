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

FORNT_STOP_DISTANCE_MM = 90
OPTICAL_LIGHT_POWER_PCT = 70 
TOUCHLED_BRIVGHTNESS = 120 
SENSOR_WARMUP_MSEC = 1000

m_brain = Brain() 
right_drive_motor = Motor(Ports.PORT6)
left_drive_motor = Motor(Ports.PORT1)
controller = Controller() 
claw = Motor(Ports.PORT4) 
arm = Motor(Ports.PORT10)
distance_sensor = Distance(Ports.PORT5)
optical_sensor = Optical(Ports.PORT2)
bumper_sensor = Bumper(Ports.PORT9)
touchled_sensor = Touchled(Ports.PORT12)

def is_front_blocked(): 
    front_near_by_distance = distance_sensor.is_object_detected() and distance_sensor.object_distance(MM) < FORNT_STOP_DISTANCE_MM 
    front_near_by_optical = optical_sensor.is_near_object() 
    return front_near_by_distance or front_near_by_optical 

def update_side_touchled(): 
    if is_front_blocked() or bumper_sensor.pressing():  
        touchled_sensor.on(Color.RED)
    else: 
        touchled_sensor.on(Color.GREEN) 

def limit_fronward_velocity(velocity): 
    if velocity > 0 and is_front_blocked(): 
        return 0 
    else: 
        return velocity 

def limit_backward_velocity(velocity): 
    if velocity < 0 and bumper_sensor.pressing(): 
        return 0 
    else: 
        return velocity 

def apply_deadband(value): 
    if abs(value)<JOYSTICK_DEADBAND: 
        return 0 
    else: 
        return value

def main(): 
    claw.set_stopping(HOLD)
    arm.set_stopping(HOLD)
    arm.set_max_torque(CLAW_MAX_TORQUE_PCT, PERCENT)

    optical_sensor.set_light_power(OPTICAL_LIGHT_POWER_PCT, PERCENT)
    touchled_sensor.set_brightness(TOUCHLED_BRIVGHTNESS)
    sleep(SENSOR_WARMUP_MSEC)

    while True: 
        right_velocity = apply_deadband(controller.axisD.position())
        right_velocity = limit_fronward_velocity(right_velocity)
        right_velocity = limit_backward_velocity(right_velocity)
        right_drive_motor.spin(REVERSE, right_velocity, PERCENT)

        left_velocity = apply_deadband(controller.axisA.position())
        left_velocity = limit_fronward_velocity(left_velocity) 
        left_velocity = limit_backward_velocity(left_velocity) 
        left_drive_motor.spin(FORWARD, left_velocity, PERCENT) 

        right_button_pressed_down = controller.buttonRUp.pressing() 
        left_button_pressed_down = controller.buttonLUp.pressing()
        right_button_position = right_button_pressed_down - left_button_pressed_down
        claw.spin(FORWARD, (right_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        right_button_pressed_up = controller.buttonRDown.pressing() 
        left_button_pressed_up = controller.buttonLDown.pressing()
        left_button_position = left_button_pressed_up - right_button_pressed_up
        arm.spin(FORWARD, (left_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        update_side_touchled() 

        sleep(LOOP_SLEEP_MSEC)

main() 