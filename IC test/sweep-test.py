import wiringpi as wiringpi  
from time import sleep  

import time
import threading
  
pin_base = 65       # lowest available starting number is 65  
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND  
i2c2_addr = 0x21 
i2c3_addr = 0x23
i2c4_addr = 0x24
i2c5_addr = 0x25  # A0, A1, A2 pins all wired to GND



# DECLARATION of wiring Pi
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c_addr)     # set up the pins and i2c address 
wiringpi.mcp23017Setup(81,i2c2_addr) 
wiringpi.mcp23017Setup(97,i2c3_addr)
wiringpi.mcp23017Setup(113,i2c4_addr)
wiringpi.mcp23017Setup(129,i2c5_addr)

# wiringpi.pinMode(65, 1)         # sets GPA0 to output  
# wiringpi.digitalWrite(65, 1)    # sets GPA0 to 0 (0V, off)  

# for i in range(65,81):
#     wiringpi.digitalWrite(i, 1)


data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# for i in range(97, 130):
for i in range(97,146):
    wiringpi.pinMode(i, 1)
    wiringpi.digitalWrite(i,1)

   

# # for i in range



# while True:
#     for i in range(65,97):
#         wiringpi.pinMode(i, 0)
#         data[i-65] = wiringpi.digitalRead(i)
#         #data[i-65] = wiringpi.digitalWrite(i,1)
#     if (data[1] ):
#         wiringpi.digitalWrite(98, 1)
#     if(data[2] ):
#         wiringpi.digitalWrite(99,1)
#     if (data[1] ==0 ):
#         wiringpi.digitalWrite(98, 0)
#     if(data[2] == 0):
#         wiringpi.digitalWrite(99,0)
#     print(data)

# for i in range(97,130):
#     print(i)
#     wiringpi.digitalWrite(i, 1)
#     time.sleep(2)

    #print(data)

"""while True:
     for i in range(64,136):
         incoming = wiringpi.digitalRead(i)
         if data[i+64] == 0 and incoming:
             print("Got turned on: ", i)
             wiringpi.digitalWrite(i,1)"""
        
  

  
# Note: MCP23017 has no internal pull-down, so I used pull-up and inverted  
# # the button reading logic with a "not"  
  
# try:  
#     while True:  
#         if not wiringpi.digitalRead(80): # inverted the logic as using pull-up  
#             wiringpi.digitalWrite(65, 1) # sets port GPA1 to 1 (3V3, on)  
#         else:  
#             wiringpi.digitalWrite(65, 0) # sets port GPA1 to 0 (0V, off)  
#         sleep(0.05)  
# finally:  
#     wiringpi.digitalWrite(65, 0) # sets port GPA1 to 0 (0V, off)  
#     wiringpi.pinMode(65, 0)      # sets GPIO GPA1 back to input Mode  
#     # GPB7 is already an input, so no need to change anything