'''This script will scan local IP addresses and report valid addresses'''

import os
import numpy as np
import time

good_addresses = []


for i in range(10000):
    os.system("cls")
    print(i)
    time.sleep(.1)
    if(os.system("ping 192.168.4.1 /n 1")==0):
        os.system("cls")
        print("Connection Successful")
        break

# for i in range(0,255):
#     for j in range(0,255):
#         IP = "192.168." + str(i) + "." + str(j) 
#         if os.system("ping " + IP + "/n 1") == 0:
#             good_addresses.append(IP)
#         os.system("cls")
#         print("Good addresses:")
#         print(good_addresses)

