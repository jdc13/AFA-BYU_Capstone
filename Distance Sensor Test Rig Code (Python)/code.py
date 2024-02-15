#Test Rig Code
#This file will write elapsed time, accelerometer/gyro data, distance sensor measurements and camera data to an SD card.
#Data dimensions:
#Time: 			1
#accelerometer: 3
#gyro: 			3
#distance:		6
#thermal cam:	24x32 (will make a 1D data field, so 768
#Total columns per line: 781

# from hardware_setup import * #hardware setup will add distance sensors to the header

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
    for i in range(8):
        try:
            vl53 = adafruit_vl53l4cd.VL53L4CD(MUX[i])
            DIST.append(vl53)
            vl53.inter_measurement = 0
            vl53.timing_budget = 11
            vl53.start_ranging()
            
            header.append( "D" + str(i))
        except:
            print("Sensor ", i, " not connected")
        print(i)



bno = BNO08X_I2C(i2c)

bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)				#Linear acceleration
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)					#angular acceleration
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)	#Absolute angular position relative to north
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR)			#relative angular position (integrated from gyro?)




pix = neopixel.NeoPixel(board.NEOPIXEL, 1)

file = 0
while True:
    #Red = sensor setup
    pix.brightness = .5
    pix.fill((225,0,0))
    
    header = ["time",
              "AX", 	"AY", 		"AZ",						#Accelerometer, (m/s)
              "RX", 	"RY", 		"RZ",						#Gyro
              "GeoI",  	"GeoJ", 	"GeoK", 	"GeoReal",		#see sensor datasheet forunits https://www.ceva-ip.com/wp-content/uploads/2019/10/BNO080_085-Datasheet.pdf
              "GameI", 	"GameJ", 	"GameK", 	"GameReal" ]
    DIST = [] #empty list of sensors
    dist_setup()
#     header.append( "THERMAL") #Add this in when the thermal camera is ready
    
#     files = vfs.ilistdir("/sd")
#     print(files)
    
    
    with open("/sd/data"+str(file)+".dat", "a") as f: #open the SD card
        def write_SD_line(line): 
            for i in line:
                f.write(str(i))
                f.write("\t")
            f.write("\r\n")

        
        write_SD_line(header)
        pix.fill((0,255,0))
        #delete the header vairable since it is no longer needed but the memory it occupies is
        del header
    
        while True:
            line = [] #create an empty list
            line.append(time.monotonic_ns()) #time stamp
            
#             line = line+ list(sensor.acceleration) + list(sensor.gyro) #IMU data
            line = line + list(bno.acceleration) + list(bno.gyro) + list(bno.geomagnetic_quaternion) + list(bno.game_quaternion)
            for d in DIST: #Distance Data
                if d.data_ready:
                    d.clear_interrupt()
                    line.append(d.distance)
                    
                else:
                    line.append("NAN")
        #     print(line)
        
#             try:
#                 pass
#                 mlx.getFrame(frame)
#             except ValueError:
#                 continue
#             
#             print(frame)
        
        
        
        
        
            write_SD_line(line)
            print(line)
            #Break and close the file if the package is upside down
            if(line[3] < -5):
                break
                
                        
        print("Program finished")
        pix.fill((0,0,255))
        file +=1
        while bno.acceleration[2] < 5:
            pass

