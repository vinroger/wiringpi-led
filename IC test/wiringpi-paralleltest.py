import wiringpi as wiringpi  
from time import sleep 
#import time 
  
pin_base = 65       # lowest available starting number is 65  
ic1_addr = 0x20     # A0, A1, A2 pins all wired to GND  
ic2_addr = 0x21     # A0, A1, A2 pins all wired to GND  
ic3_addr = 0x22     # A0, A1, A2 pins all wired to GND  
 
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,ic1_addr)
wiringpi.mcp23017Setup(82,ic2_addr)
wiringpi.mcp23017Setup(98,ic3_addr)

# #IC CHIP 1 Declaration
# ic1.wiringPiSetup()                   
# ic1.mcp23017Setup(pin_base,ic1_addr)   
# #IC CHIP 2 Declaration
# ic2.wiringPiSetup()                    
# ic2.mcp23017Setup(pin_base,ic2_addr)   
# #IC CHIP 3 Declaration
# ic3.wiringPiSetup()                    # initialise wiringpi  
# ic3.mcp23017Setup(pin_base,ic3_addr)   # set up the pins and i2c address 

#Every 70 to 82 pins on ic1 ic2 ic3 is set to OUTPUT
# for i in range(70,82):
#     ic1.pinMode(i, 0)
#     ic2.pinMode(i, 0)
#     ic3.pinMode(i, 0)

#pin 65 66 in 3 ics is set to OUTPUT
# for i in [ic1, ic2, ic3]:
#     i.pinMode(65, 1)
#     i.pinMode(66, 1)

# #pin 67 on ic3 is set to INPUT
# ic3.pinMode(67, 0)
# ic3.pullUpDnControl(80, 2)
for j in [65, 66, 82, 83, 98, 99]:
    wiringpi.pinMode(j,1)

# wiringpi.pinMode(101, 0)
# wiringpi.pullUpDnControl(101, 2)

def all_off():
    for j in [65, 66, 82, 83, 98, 99]:
        wiringpi.digitalWrite(j, 0)
# #*swoop swoop go whoop whoop*
def sweepLED():
    for j in [65, 66, 82, 83, 98, 99]:
        wiringpi.digitalWrite(j, 1)
        sleep(0.05)


#all_off()

while True:
    #print(wiringpi.digitalRead(100))
    if (wiringpi.digitalRead(100) == 1):
        sweepLED()
    else:
        all_off()



# wiringpi.pinMode(84, 1)
# wiringpi.digitalWrite(84,1)
#all_off()
# for i in [65, 82, 98]:

#     wiringpi.pinMode(i, 1)         # sets GPA0 to output  
#     wiringpi.digitalWrite(i, 1)




# wiringpi.pinMode(65, 0)         # sets GPB7 to input  
# wiringpi.pullUpDnControl(65, 2) # set internal pull-up 

# while True:
#     print(wiringpi.digitalRead(65))

