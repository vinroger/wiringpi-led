import wiringpi as wiringpi  
from time import sleep  
import pygame

import time
import thPianoReading
  
pin_base = 65       # lowest available starting number is 65  
# i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND   
# i2c2_addr = 0x21
# i2c3_addr = 0x23
# i2c4_addr = 0x24
i2c5_addr = 0x25

# DECLARATION of wiring Pi
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c5_addr)     # set up the pins and i2c address 
# wiringpi.mcp23017Setup(81,i2c2_addr) 
# wiringpi.mcp23017Setup(97,i2c3_addr)
# wiringpi.mcp23017Setup(113,i2c4_addr)
#wiringpi.mcp23017Setup(129,i2c5_addr)

# for i in range(129, 150):
#     wiringpi.pinMode(i,1)
#     wiringpi.digitalWrite(i,1)

buttonPianoPin = [
    1,2,3,4,5,6,7,8
]
ledPianoPin = [
    1,2,3,4,5,6,7,8
]

#Declaring button as an i2C input
for i in range(8):
    wiringpi.pinMode(buttonPianoPin[i], 0)

#Declaring LED as an i2c output
for i in range(8):
    wiringpi.pinMode(ledPianoPin[i], 0)


#pygame init
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


#variables
buttonsPianoReading = [0,0,0,0,0,0,0,0]
flagPianoPressedState = [
    [0, 0, 0, 0, 0, 0, 0, 0]
]

#declaration
noteduration = [1, 1, 1, 1, 1, 1, 1, 1] #in second


# for i in range(73, 83):
#     wiringpi.pinMode(i, 1)
#     wiringpi.digitalWrite(i, 1)
# while True:
#     for i in range(65,73):
#         wiringpi.pinMode(i, 0)
#         buttonsPianoReading[i-65] = wiringpi.digitalRead(i)
#     print(buttonsPianoReading)

def play_note(i):
    while buttonsPianoReading[i]:
        notefiles[i].play()
        time.sleep(noteduration[i])
    return

def updateButtonsPianoReading():
    global buttonsPianoReading
    global flagPianoPressedState
    for i in range(4):
       
        newPianoReading = wiringpi.digitalRead(buttonPinLocation[i])
        #print(buttonsPianoReading)
        # if recent/prev is 0 then new/next is 1, meaning button get turned on
        if ((buttonsPianoReading[i] == 0) and (newPianoReading == 1) and flagPianoPressedState[i]== 0):
            flagPianoPressedState[i] = 1
            buttonsPianoReading[i] = 1
            #thPianoReading
            t3 = threading.Thread(target=play_note, args=[i])
            t3.start()

        elif ((buttonsPianoReading[i] == 1) and (newPianoReading == 0)and flagPianoPressedState[i]== 1):
            #print("1,0,1")
            flagPianoPressedState[i] = 0

        # if recent/prev is 1 then new/next is 1, meaning button get turned off
        elif (buttonsPianoReading[i] == 1 and newPianoReading == 1 and flagPianoPressedState[i]== 0 ):
            flagPianoPressedState[i]= 1 
            buttonsPianoReading[i] = 0

def updatePianoLed():
    for i in range(4):
        wiringpi.digitalWrite(ledPianoPin[i], buttonsPianoReading[i])

while True:
    updateButtonsPianoReading()
    updatePianoLed()

