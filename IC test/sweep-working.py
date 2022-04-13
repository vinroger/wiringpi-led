import wiringpi as wiringpi  
from time import sleep  
import threading
import time
  
pin_base = 65       # lowest available starting number is 65  
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND  
i2c2_addr = 0x21 
i2c3_addr = 0x23
i2c4_addr = 0x24
i2c5_addr = 0x25
  
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


# for i in range(97, 129):
    
#     wiringpi.pinMode(i, 1)
#     wiringpi.digitalWrite(i,0)
    
#wiringpi.digitalWrite(99,1)
# # for i in range



buttonPinLocation = [
    [92, 96, 88, 81, 68, 72, 76, 79],
    [91, 95, 85, 82, 67, 71, 75, 80],
    [90, 94, 86, 83, 66, 70, 74, 78],
    [89, 93, 87, 84, 65, 69, 73, 77]
]

ledPinLocation = [
    [116, 120, 121, 105, 99, 104, 109, 128],
    [115, 119, 124, 127, 100, 103, 108, 112],
    [114, 118, 123, 126, 98, 102, 107, 111],
    [113, 117, 122, 125, 97, 101, 106, 110]
]

button_dict = {}
for row in range(4):
    for col in range(8):
        button_dict[buttonPinLocation[row][col]] = [row, col]

def setled(pin, value):
    wiringpi.digitalWrite(pin,value)


sleeptime= 0.05
def sweep_forward(col):
    for i in range(col,8 ):
        for j in range(4):
            setled(ledPinLocation[j][i], 1)
        time.sleep(sleeptime)
        for j in range(4):
            setled(ledPinLocation[j][i], 0)
        time.sleep(sleeptime)

def sweep_backward(col):
    for i in range(col,-1,-1 ):
        for j in range(4):
            setled(ledPinLocation[j][i], 1)
        time.sleep(sleeptime)
        for j in range(4):
            setled(ledPinLocation[j][i], 0)
        time.sleep(sleeptime)

# sweep_forward(7)
# sweep_backward(0)
       

while True:
    for i in range(65,97):
        incoming = wiringpi.digitalRead(i)
        if incoming:
            t2 = threading.Thread(target=sweep_forward, args=[button_dict[i][1]])
            t2.start()
            t3 = threading.Thread(target=sweep_backward, args=[button_dict[i][1]])
            t3.start()
            #print("Got turned on: ",button_dict[i] )
            # wiringpi.digitalWrite(i,1)
            
    
  

  
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