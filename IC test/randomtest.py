import wiringpi as wiringpi  
from time import sleep  

import time
import threading
  
pin_base = 65       # lowest available starting number is 65  
# i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND   
# i2c2_addr = 0x21
# i2c3_addr = 0x23
# i2c4_addr = 0x24
i2c5_addr = 0x25

  
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c5_addr)     # set up the pins and i2c address 
# wiringpi.mcp23017Setup(81,i2c2_addr) 
# wiringpi.mcp23017Setup(97,i2c3_addr)
# wiringpi.mcp23017Setup(113,i2c4_addr)
#wiringpi.mcp23017Setup(129,i2c5_addr)

# for i in range(129, 150):
#     wiringpi.pinMode(i,1)
#     wiringpi.digitalWrite(i,1)
data = [0,0,0,0,0,0,0,0]
for i in range(73, 83):
    wiringpi.pinMode(i, 1)
    wiringpi.digitalWrite(i, 1)
while True:
    for i in range(65,73):
        wiringpi.pinMode(i, 0)
        data[i-65] = wiringpi.digitalRead(i)
    print(data)




