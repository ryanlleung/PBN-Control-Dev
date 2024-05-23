
import time
from sync_dual import *

"""
Change DEVICENAME in sync_dual.py
Make sure the Dynamixel port is not occupied by another software.
Check sync_dual.py for more info.
"""

#### DONT CHANGE START ####
dnx = Dynamixel()
dnx.open_port()

dnx.enable_torque(DXL1_ID)
dnx.enable_torque(DXL2_ID)
##### DONT CHANGE END #####


#### Velocity Demo 1 mm/s = 3.33 unit/second ####
"""
Sets the goal velocity of a Dynamixel motor.

Parameters:
id (int): The ID of the Dynamixel motor.
velocity (int): The goal velocity to set in 0.02398 rad/s units.
"""
dnx.set_velocity(DXL2_ID, 33.3)
time.sleep(5)
dnx.set_velocity(DXL2_ID, 0)
time.sleep(2)


#### Dualvel Demo 1 mm/s = 3.33 unit/second ####
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
# dnx.set_dualvel(3.33, 3.33, 1)
# dnx.set_dualvel(-3.33, -3.33, 1)
# dnx.set_dualvel(3.33, 0, 1)
# dnx.set_dualvel(-3.33, 0, 1)
# dnx.set_dualvel(0, 3.33, 1)
# dnx.set_dualvel(0, -3.33, 1)


#### Profile velocity and acceleration Demo ####
"""
Position mode where the motor moves to a specified position.
Set the profile velocity and acceleration of the motor when moving to a position.
"""
# dnx.set_mode(DXL1_ID, "extpos")
# dnx.set_mode(DXL2_ID, "extpos")

# dnx.set_profile_acceleration(DXL1_ID, 20)
# dnx.set_profile_acceleration(DXL2_ID, 20)
# dnx.set_profile_velocity(DXL1_ID, 200)
# dnx.set_profile_velocity(DXL2_ID, 200)

# dnx.set_position(DXL1_ID, 1000)
# dnx.set_position(DXL2_ID, 1000)
# time.sleep(5)
# print(f"Position 1: {dnx.get_position(DXL1_ID)-dnx.motor1_pos0}, Position 2: {dnx.get_position(DXL2_ID)-dnx.motor2_pos0}")
# dnx.set_position(DXL1_ID, 0)
# dnx.set_position(DXL2_ID, 0)
# time.sleep(5)
# print(f"Position 1: {dnx.get_position(DXL1_ID)-dnx.motor1_pos0}, Position 2: {dnx.get_position(DXL2_ID)-dnx.motor2_pos0}")


#### Current-based position control Demo ####
"""
Current-based position control mode where the motor moves to a specified position.
Set the current limit, profile velocity, and profile acceleration of the motor when moving to a position.
"""
# dnx.set_current_limit(DXL1_ID, 50)
# dnx.set_current_limit(DXL2_ID, 50)

# dnx.set_profile_acceleration(DXL1_ID, 1)
# dnx.set_profile_acceleration(DXL2_ID, 1)
# dnx.set_profile_velocity(DXL1_ID, 10)
# dnx.set_profile_velocity(DXL2_ID, 10)

# dnx.home_position(DXL1_ID)
# dnx.home_position(DXL2_ID)

# dnx.set_dualpos(500, 500, "curpos")
# time.sleep(5)
# print(f"Position 1: {dnx.get_position(DXL1_ID)-dnx.motor1_pos0}, Position 2: {dnx.get_position(DXL2_ID)-dnx.motor2_pos0}")

# dnx.set_dualpos(0, 0, "curpos")
# time.sleep(5)
# print(f"Position 1: {dnx.get_position(DXL1_ID)-dnx.motor1_pos0}, Position 2: {dnx.get_position(DXL2_ID)-dnx.motor2_pos0}")


#### DONT CHANGE START ####
dnx.disable_torque(DXL1_ID)
dnx.disable_torque(DXL2_ID)
dnx.close_port()
##### DONT CHANGE END #####
