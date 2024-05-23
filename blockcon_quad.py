
import time
from sync_quad import *

"""
Change DEVICENAME in sync_quad.py
Make sure the Dynamixel port is not occupied by another software.
Check sync_dual.py for more info.
"""

#### DONT CHANGE START ####
dnx = DynamixelQuad()
dnx.open_port()

dnx.enable_torque(DXL1_ID)
dnx.enable_torque(DXL2_ID)
dnx.enable_torque(DXL3_ID)
dnx.enable_torque(DXL4_ID)
##### DONT CHANGE END #####


#### Velocity Demo 1 mm/s = 3.33 unit/second ####
"""
Sets the goal velocity of a Dynamixel motor.

Parameters:
id (int): The ID of the Dynamixel motor.
velocity (int): The goal velocity to set in 0.02398 rad/s units.
"""
# dnx.set_velocity(DXL2_ID, 33.3)
# time.sleep(2)
# dnx.set_velocity(DXL2_ID, 0)
# time.sleep(2)


#### Quadvel Demo 1 mm/s = 3.33 unit/second ####
"""
Sets the velocities of two Dynamixel motors simultaneously for a specified duration.

Parameters:
vel1 (int): The target velocity for the first motor (in Dynamixel velocity units).
vel2 (int): The target velocity for the second motor (in Dynamixel velocity units).
dur (float): The duration for which the motors should run at the specified velocities (in seconds).
brake (bool): If True, the motors will stop (brake) after the specified duration. If False, the motors will be disabled after the duration.

Returns:
None
"""
# dnx.set_quadvel(33.3, 33.3, 33.3, 33.3, 2)
# dnx.set_quadvel(-33.3, -33.3, -33.3, -33.3, 2)
# dnx.set_quadvel(33.3, 0, 0, 0, 2)
# dnx.set_quadvel(0, 33.3, 0, 0, 2)
# dnx.set_quadvel(0, 0, 33.3, 0, 2)
# dnx.set_quadvel(0, 0, 0, 33.3, 2)
# dnx.set_quadvel(0, 0, 0, 0, 2)


#### Dualpos Demo ####
dnx.set_current_limit(DXL1_ID, 800)
dnx.set_current_limit(DXL2_ID, 800)
dnx.set_current_limit(DXL3_ID, 800)
dnx.set_current_limit(DXL4_ID, 800)

dnx.set_profile_acceleration(DXL1_ID, 1)
dnx.set_profile_acceleration(DXL2_ID, 1)
dnx.set_profile_acceleration(DXL3_ID, 1)
dnx.set_profile_acceleration(DXL4_ID, 1)
dnx.set_profile_velocity(DXL1_ID, 10)
dnx.set_profile_velocity(DXL2_ID, 10)
dnx.set_profile_velocity(DXL3_ID, 10)
dnx.set_profile_velocity(DXL4_ID, 10)

dnx.home_position(DXL1_ID)
dnx.home_position(DXL2_ID)
dnx.home_position(DXL3_ID)
dnx.home_position(DXL4_ID)

dnx.set_quadpos(500, 500, 500, 500, "extpos")
time.sleep(5)
print(f"Position 1: {dnx.get_position(DXL1_ID) - dnx.motor1_pos0}, "
      f"Position 2: {dnx.get_position(DXL2_ID) - dnx.motor2_pos0}, "
      f"Position 3: {dnx.get_position(DXL3_ID) - dnx.motor3_pos0}, "
      f"Position 4: {dnx.get_position(DXL4_ID) - dnx.motor4_pos0}")

dnx.set_quadpos(0, 0, 0, 0, "extpos")
time.sleep(5)
print(f"Position 1: {dnx.get_position(DXL1_ID) - dnx.motor1_pos0}, "
      f"Position 2: {dnx.get_position(DXL2_ID) - dnx.motor2_pos0}, "
      f"Position 3: {dnx.get_position(DXL3_ID) - dnx.motor3_pos0}, "
      f"Position 4: {dnx.get_position(DXL4_ID) - dnx.motor4_pos0}")


#### DONT CHANGE START ####
dnx.disable_torque(DXL1_ID)
dnx.disable_torque(DXL2_ID)
dnx.disable_torque(DXL3_ID)
dnx.disable_torque(DXL4_ID)
dnx.close_port()
##### DONT CHANGE END #####
