
import os
import sys
import serial
import threading
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg

from opten_lib import *
from sync_dual import *
from datetime import datetime
      
        
#### Motor Init ####

print("\nStarting motors initialisation")

dnx = Dynamixel()
dnx.open_port()

dnx.enable_torque(DXL1_ID)
dnx.enable_torque(DXL2_ID)

#### Opten Init ####

opt = OpticalDuo()
opt.start_camera()

####################################################################################################

class DataLogger(threading.Thread):
    
    def __init__(self, motor1_pos0, motor2_pos0):
        super().__init__()
        self.opt = opt
        self.dnx = dnx
        self.time_data = np.array([])
        self.time_start = time.time()
        self.motor1_pos0 = motor1_pos0
        self.motor2_pos0 = motor2_pos0
        self.motor1_apos_data, self.motor2_apos_data = np.array([]), np.array([])
        self.motor1_cur_data, self.motor2_cur_data = np.array([]), np.array([])
        self.camera1_data = np.empty((0, 36, 36))
        self.camera2_data = np.empty((0, 36, 36))
        self.pause_poll = False
        self.running = True
    
    def run(self):
        while self.running:
            if not self.pause_poll:
                motor1_apos = (dnx.get_position(DXL1_ID) - motor1_pos0) / 52
                motor2_apos = (dnx.get_position(DXL2_ID) - motor2_pos0) / 52
                motor1_cur = dnx.get_current(DXL1_ID)
                motor2_cur = dnx.get_current(DXL2_ID)
                self.motor1_apos_data = np.append(self.motor1_apos_data, motor1_apos)
                self.motor2_apos_data = np.append(self.motor2_apos_data, motor2_apos)
                self.motor1_cur_data = np.append(self.motor1_cur_data, motor1_cur)
                self.motor2_cur_data = np.append(self.motor2_cur_data, motor2_cur)
                self.camera1_data = np.vstack((self.camera1_data, [self.opt.serial_reader1.pixels]))
                self.camera2_data = np.vstack((self.camera2_data, [self.opt.serial_reader2.pixels]))
                self.time_data = np.append(self.time_data, time.time() - self.time_start)
                time.sleep(0.08)
            else:
                time.sleep(0.01)
                
    def set_velocity(self, id, velocity):
        self.pause_poll = True
        time.sleep(0.05)
        dnx.set_velocity(id, velocity)
        time.sleep(0.05)
        self.pause_poll = False
        
    def set_2velocity(self, velocity1, velocity2):
        self.pause_poll = True
        time.sleep(0.05)
        dnx.set_velocity(DXL1_ID, velocity1)
        time.sleep(0.05)
        dnx.set_velocity(DXL2_ID, velocity2)
        time.sleep(0.05)
        self.pause_poll = False
        
    def set_position(self, id, position):
        self.pause_poll = True
        time.sleep(0.05)
        dnx.set_position(id, position)
        time.sleep(0.05)
        self.pause_poll = False
            
    def save(self, filename=None):
        print(f"Length of data: {len(self.time_data)}")
        print(f"Length of camera1 data: {len(self.camera1_data)}")
        print(f"Length of camera2 data: {len(self.camera2_data)}")
        
        df = pd.DataFrame({'Time': np.round(self.time_data, 3),
                            'Motor1 Pos': np.round(self.motor1_apos_data, 3),
                            'Motor1 Cur': np.round(self.motor1_cur_data, 3),
                            'Motor2 Pos': np.round(self.motor2_apos_data, 3),
                            'Motor2 Cur': np.round(self.motor2_cur_data, 3)})
        
        # Flatten the camera data
        flat_camera1_data = [frame.flatten() for frame in self.camera1_data]
        flat_camera2_data = [frame.flatten() for frame in self.camera2_data]
        
        # Create column names for the camera pixel data
        camera1_columns = [f'Camera1_Pixel_{i}' for i in range(flat_camera1_data[0].size)]
        camera2_columns = [f'Camera2_Pixel_{i}' for i in range(flat_camera2_data[0].size)]
        
        df_camera1 = pd.DataFrame(flat_camera1_data, columns=camera1_columns)
        df_camera2 = pd.DataFrame(flat_camera2_data, columns=camera2_columns)
        
        df = pd.concat([df, df_camera1, df_camera2], axis=1)                    
        
        os.makedirs('./exports', exist_ok=True)
        if not filename:
            filename = f"./exports/camstream_{datetime.fromtimestamp(self.time_start).strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        return filename
        
    def stop(self):
        self.running = False
        
motor1_pos0 = dnx.get_position(DXL1_ID)
motor2_pos0 = dnx.get_position(DXL2_ID)

dnx.set_mode(DXL1_ID, "extpos")
dnx.set_mode(DXL2_ID, "extpos")
dnx.set_profile_acceleration(DXL1_ID, 1)
dnx.set_profile_acceleration(DXL2_ID, 1)
dnx.set_profile_velocity(DXL1_ID, 1)
dnx.set_profile_velocity(DXL2_ID, 1)

logger = DataLogger(motor1_pos0, motor2_pos0)
logger.start()
print("Data logger started")                


#### Motor Movement ####

time.sleep(1)
logger.set_position(DXL1_ID, motor1_pos0 + 1000)
logger.set_position(DXL2_ID, motor2_pos0 + 1000)
time.sleep(100)
logger.set_2velocity(0, 0)


filename = logger.save()
logger.stop()
logger.join()


####################################################################################################

#### Opten Close ####

opt.close()

#### Motor Close ####

print("\nClosing motors")

dnx.disable_torque(DXL1_ID)
dnx.disable_torque(DXL2_ID)
dnx.close_port()
