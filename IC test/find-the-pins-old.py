import wiringpi as wiringpi  
from time import sleep 
#import time 
  
pin_base = 65       # lowest available starting number is 65  
ic1_addr = 0x20     # A0, A1, A2 pins all wired to GND  
ic2_addr = 0x21     # A0, A1, A2 pins all wired to GND  
ic3_addr = 0x22     # A0, A1, A2 pins all wired to GND  
ic4_addr = 0x23
 
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,ic1_addr)
wiringpi.mcp23017Setup(82,ic2_addr)
wiringpi.mcp23017Setup(99,ic3_addr)
wiringpi.mcp23017Setup(116,ic4_addr)

for j in range(99,117):
    wiringpi.pinMode(65, 1)         # sets GPA0 to output  
    wiringpi.digitalWrite(j, 1)