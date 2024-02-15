#Software Libraries:
import ulab.numpy as np
import time
import os

#Hardware libraries:
import board		#General Functions
import busio		#Comms Bus
# from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS #IMU
import adafruit_bno08x #IMU
from adafruit_bno08x.i2c import BNO08X_I2C #IMU
import sdioio		#SD Card
import storage		#File system for SD card
import adafruit_TCA9548A as TCA #MUX
import adafruit_vl53l4cd #Distance sensor
import neopixel


#Initialize the SD Card
sdcard = sdioio.SDCard(
    clock = board.SDIO_CLOCK,
    command=board.SDIO_COMMAND,
    data=board.SDIO_DATA,
    frequency = 25000000)
#initialize the file system
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


i2c = board.I2C()  # uses board.SCL and board.SDA


#initialize IMU





# from adafruit_lsm6ds import Rate, AccelRange, GyroRange
# 
# from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
# 
# 
# sensor = LSM6DS(i2c)

# sensor.accelerometer_range = AccelRange.RANGE_8G
# print(
#     "Accelerometer range set to: %d G" % AccelRange.string[sensor.accelerometer_range]
# )
# 
# sensor.gyro_range = GyroRange.RANGE_2000_DPS
# print("Gyro range set to: %d DPS" % GyroRange.string[sensor.gyro_range])
# 
# sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
# # sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
# print("Accelerometer rate set to: %d HZ" % Rate.string[sensor.accelerometer_data_rate])
# 
# sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
# print("Gyro rate set to: %d HZ" % Rate.string[sensor.gyro_data_rate])

    
#Create the MUX object
MUX = TCA.TCA9548A(i2c)

def dist_setup():
    #Create each sensor that is connected to the MUX using the MUX object instead of I2C
    for i in range(7):
        try:
            vl53 = adafruit_vl53l4cd.VL53L4CD(MUX[i])
            DIST.append(vl53)
            vl53.inter_measurement = 20
            vl53.timing_budget = 17
            vl53.start_ranging()
            
            header.append( "D" + str(i))
        except:
            print("Sensor ", i, " not connected")
        print(i)



# bno = BNO08X_I2C(MUX[7])
# 
# bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)				#Linear acceleration
# bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)					#angular acceleration
# bno.enable_feature(adafruit_bno08x.BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)	#Absolute angular position relative to north
# bno.enable_feature(adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR)			#relative angular position (integrated from gyro?)
