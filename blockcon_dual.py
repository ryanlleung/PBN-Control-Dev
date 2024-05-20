
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
time.sleep(2)
dnx.set_velocity(DXL2_ID, 0)
time.sleep(2)


## Dualvel Demo 1 mm/s = 3.33 unit/second ##
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
dnx.set_dualvel(3.33, 3.33, 1)
dnx.set_dualvel(-3.33, -3.33, 1)
dnx.set_dualvel(3.33, 0, 1)
dnx.set_dualvel(-3.33, 0, 1)
dnx.set_dualvel(0, 3.33, 1)
dnx.set_dualvel(0, -3.33, 1)



#### DONT CHANGE START ####
dnx.disable_torque(DXL1_ID)
dnx.disable_torque(DXL2_ID)
dnx.close_port()
##### DONT CHANGE END #####
