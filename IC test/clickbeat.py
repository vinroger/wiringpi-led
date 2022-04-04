import wiringpi as wiringpi  
from time import sleep 
#import time 
  
pin_base = 65       # lowest available starting number is 65  
ic1_addr = 0x20     # A0, A1, A2 pins all wired to GND  
ic2_addr = 0x21     # A0, A1, A2 pins all wired to GND  
ic3_addr = 0x22     # A0, A1, A2 pins all wired to GND  


button_input_pin = [
[65,66,67,68,69,70,71,72],
[73,74,75,76,77,78,79,80],
[81,82,83,84,85,86,87,88],
[89,90,91,92,93,94,95,96]
]

led_output_pin = [
[97,98,99,100,101,102,103,104],
[105,106,107,108,109,110,111,112],
[113,114,115,116,117,118,119,120],
[120,121,122,123,124,125,126,127]
]
 
#DECLARATION of wiring Pi
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,ic1_addr)
wiringpi.mcp23017Setup(82,ic2_addr)
wiringpi.mcp23017Setup(98,ic3_addr)
wiringpi.mcp23017Setup(115,ic3_addr)

## Declaring button input as an i2C input 
for i in range(4):
    for j in range(8):
        wiringpi.pinMode(button_input_pin[i][j], 0)

#Array for pressed or not pressed readings
readings = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]
]

### Check for input
def update_readings():
    for i in range(4):
        for j in range(8):
            data = wiringpi.digitalRead(button_input_pin[i][j])
            ex = readings[i][j]
            if (ex == 0 and data == 1):
                ex = 1
            elif (ex == 1 and data == 0):
                ex = 0
            else : 
                pass

def update_led():
    for i in range(4):
        for i in range(8):
            wiringpi.digitalWrite(button_input_pin[i][j], readings[i][j])


while True:
    update_readings()
    updata_led()




            


