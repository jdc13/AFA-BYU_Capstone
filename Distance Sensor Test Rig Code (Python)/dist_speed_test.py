import hardware_setup
import time

def dist_setup():
    #Create each sensor that is connected to the MUX using the MUX object instead of I2C
    for i in range(7):
        try:
            vl53 = adafruit_vl53l4cd.VL53L4CD(MUX[i])
            DIST.append(vl53)
            vl53.inter_measurement = 20
            vl53.timing_budget = 18
            vl53.start_ranging()
            
        except:
            print("Sensor ", i, " not connected")
        print(i)
DIST = [] #empty list of sensors
dist_setup()

while(1):
        t_old = time.monotonic_ns()
        
        for d in DIST: #Distance Data
                if d.data_ready:
                    d.clear_interrupt()
                    t_now =time.monotonic_ns()
                    print(t_now-t_old)
                    t_old = t_n
                    
                
        
    
    