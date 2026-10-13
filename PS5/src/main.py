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

#디버그 신호들
JOYSTICK_DEADBAND = 15
BUTTON_MOTOR_SPEED = 100
LOOP_SLEEP_MSEC = 20
CLAW_MAX_TORQUE_PCT = 20
FORNT_STOP_DISTANCE_MM = 80
BACK_STOP_DISTANCE_MM = 80
OPTICAL_LIGHT_POWER_PCT = 70 
TOUCHLED_BRIVGHTNESS = 120 
SENSOR_WARMUP_MSEC = 1000

#로봇 조정 신호들
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

#디버그&추가 기능들(센서, 추가 신호, ...)

    #추가 신호
def is_blocked_anyway() -> bool: 
    return bool(is_front_blocked() or is_back_blocked()) 

    #추가 신호
def is_front_blocked() -> bool: 
    front_near_by_distance = distance_sensor.is_object_detected() and distance_sensor.object_distance(MM) < FORNT_STOP_DISTANCE_MM 
    front_near_by_optical = optical_sensor.is_near_object() 
    return front_near_by_distance or front_near_by_optical 

    #추가 신호
def is_back_blocked() -> bool:
    return bool(bumper_sensor.pressing()) 

     #추가 신호
def update_side_touchled(): 
   color_choice = Color.RED if (is_blocked_anyway) else Color.GREEN 
   touchled_sensor.on(color_choice) 

    #추가 신호 
def limit_forward_velocity(velocity, forward_block_condition: bool):
    return 0 if (velocity > 0 and forward_block_condition) else velocity

    #추가 신호
def limit_backward_velocity(velocity, rear_block_condition: bool): 
   return 0 if (velocity < 0 and rear_block_condition) else velocity 

    #추가신호
def apply_deadband(value): 
   return 0 if (abs(value) < JOYSTICK_DEADBAND) else value

    #디버그
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
    moter.spin(FORWARD, velocity, PERCENT) 

    #디버그
def reset_debug_screen(title): 
    m_brain.screen.clear_screen() 
    m_brain.screen.set_cursor(1, 1) 
    m_brain.screen.print(title)  
    m_brain.screen.next_row() 

    #디버그
def write_debug_line(label, value):
    m_brain.screen.print(label) 
    m_brain.screen.print(": ") 
    m_brain.screen.print(value)  
    m_brain.screen.next_row() 

    #디버그
def show_sensor_debug(): 
    reset_debug_screen("Sensor4 Debug") 
    
    #센서
    if not distance_sensor.installed(): 
        write_debug_line("DistOK", False) 

    #센서
    if not optical_sensor.installed(): 
            write_debug_line("OptOK", False) 

    #센서
    if not bumper_sensor.installed(): 
            write_debug_line("BumpOK", False) 

#센서
def main(): 

    #동작 고정
    claw.set_stopping(HOLD)
    arm.set_stopping(HOLD)
    arm.set_max_torque(CLAW_MAX_TORQUE_PCT, PERCENT)

    #센서
    optical_sensor.set_light_power(OPTICAL_LIGHT_POWER_PCT, PERCENT)
    touchled_sensor.set_brightness(TOUCHLED_BRIVGHTNESS)
    sleep(SENSOR_WARMUP_MSEC)

    #컨트롤러 조작
    while True: 
        spin_drive_motor(right_drive_motor, controller.axisD, REVERSE, is_front_blocked(), is_back_blocked()) 

        spin_drive_motor(left_drive_motor, controller.axisA, FORWARD, is_front_blocked(), is_back_blocked()) 


        right_button_pressed_up = controller.buttonRDown.pressing() 
        left_button_pressed_up = controller.buttonLDown.pressing()
        left_button_position = left_button_pressed_up - right_button_pressed_up
        arm.spin(FORWARD, (left_button_position) * BUTTON_MOTOR_SPEED, PERCENT)

        update_side_touchled() 

        show_sensor_debug() 
main() 
