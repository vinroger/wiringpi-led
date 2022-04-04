import wiringpi as wiringpi  
from time import sleep 
#import time 
  
pin_base = 65       # lowest available starting number is 65  
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND  
  
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c_addr)   # set up the pins and i2c address  

# outpin = 73
  
# wiringpi.pinMode(outpin, 1)         # sets GPA0 to output  
# wiringpi.digitalWrite(outpin, 1)    # sets GPA0 to 0 (0V, off)  

wiringpi.pinMode(65, 0)         # sets GPB7 to input  
wiringpi.pullUpDnControl(65, 2) # set internal pull-up 

while True:
    print(wiringpi.digitalRead(65))
    


# def off_everything():
#     for i in range(65, 74):
#         wiringpi.pinMode(i, 1) 
#         wiringpi.digitalWrite(i, 0)


# off_everything()

#while True:
    # wiringpi.digitalWrite(outpin,0)
    # sleep(1)
    #wiringpi.digitalWrite(outpin,1)
    #sleep(1)
  
# wiringpi.pinMode(80, 0)         # sets GPB7 to input  
# wiringpi.pullUpDnControl(80, 2) # set internal pull-up   
  
# Note: MCP23017 has no internal pull-down, so I used pull-up and inverted  
# the button reading logic with a "not"  
  
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