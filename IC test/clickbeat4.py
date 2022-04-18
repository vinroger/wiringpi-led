import wiringpi as wiringpi
from time import sleep
import copy
import os
import datetime
import time
import threading
import pygame
import time
import RPi.GPIO as GPIO
#import time


# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# one for button switch
GPIO.setup(4, GPIO.IN)
# one for button LED
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)


pin_base = 65       # lowest available starting number is 65
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND
i2c2_addr = 0x21
i2c3_addr = 0x23
i2c4_addr = 0x24
i2c5_addr = 0x25  # A0, A1, A2 pins all wired to GND


# DECLARATION of wiring Pi
wiringpi.wiringPiSetup()                    # initialise wiringpi
# set up the pins and i2c address
wiringpi.mcp23017Setup(pin_base, i2c_addr)
wiringpi.mcp23017Setup(81, i2c2_addr)
wiringpi.mcp23017Setup(97, i2c3_addr)
wiringpi.mcp23017Setup(113, i2c4_addr)
wiringpi.mcp23017Setup(129, i2c5_addr)

# Declaring audio files wav etc
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

beats_volume = 0.5

crash = pygame.mixer.Sound('wav/crash.wav')
pygame.mixer.Sound.set_volume(crash, beats_volume)
kick = pygame.mixer.Sound('wav/kick.wav')
pygame.mixer.Sound.set_volume(kick, beats_volume)
snare = pygame.mixer.Sound('wav/snare.wav')
pygame.mixer.Sound.set_volume(snare, beats_volume)
hihat = pygame.mixer.Sound('wav/hihat.wav')
pygame.mixer.Sound.set_volume(hihat, beats_volume)
audiofiles = [crash, hihat, snare, kick]


# Declaring misc variables
timeoutSec = 300
# to avoid start button being pressed again and turns everything off,
# we set a timeout to atleast play some beats loop before the user can turn off the beats by pressing the start button again
minimumSec = 2
beatsPause = 230
stopButtonPressed = False


buttonPinLocation = [
    [92, 96, 88, 81, 68, 72, 76, 79],
    [91, 95, 85, 82, 67, 71, 75, 80],
    [90, 94, 86, 83, 66, 70, 74, 78],
    [89, 93, 87, 84, 65, 69, 73, 77]
]

ledPinLocation = [
    [116, 119, 121, 105, 99, 104, 109, 124],
    [115, 120, 128, 127, 100, 103, 108, 112],
    [114, 118, 123, 126, 98, 102, 107, 111],
    [113, 117, 122, 125, 97, 101, 106, 110]
]

###################################################################################################################
buttonPianoPin = [
    129, 130, 131, 132, 133, 134, 135, 136
]
ledPianoPin = [
    137, 138, 139, 140, 141, 142, 143, 144
]

# Declaring button as an i2C input
for i in range(8):
    wiringpi.pinMode(buttonPianoPin[i], 0)

# Declaring LED as an i2c output
for i in range(8):
    wiringpi.pinMode(ledPianoPin[i], 1)

# variables
buttonsPianoReading = [0, 0, 0, 0, 0, 0, 0, 0]
flagPianoPressedState = [
    0, 0, 0, 0, 0, 0, 0, 0
]

# declaration
noteduration = [0.5 for i in range(8)]  # in second

# declaring music for piano
p1c = pygame.mixer.Sound('note/1c.wav')
p2d = pygame.mixer.Sound('note/2d.wav')
p3e = pygame.mixer.Sound('note/3e.wav')
p4f = pygame.mixer.Sound('note/4f.wav')
p5g = pygame.mixer.Sound('note/5g.wav')
p6a = pygame.mixer.Sound('note/6a.wav')
p7b = pygame.mixer.Sound('note/7b.wav')
p8c = pygame.mixer.Sound('note/8c.wav')

notefiles = [p1c,p2d,p3e,p4f,p5g,p6a,p7b,p8c]


def play_note(i):
    notefiles[i].play()
    while True:
        if(not buttonsPianoReading[i]):
            #print("not pressed")
            pygame.mixer.Sound.set_volume(notefiles[i], 0)
            return
        else:
            pass
            #print("pressed")
            
    return


def updateButtonsPianoReading():
    global buttonsPianoReading
    global flagPianoPressedState
    for i in range(8):
        newReading = wiringpi.digitalRead(buttonPianoPin[i])
        if (not(buttonsPianoReading[i])) and newReading:
            buttonsPianoReading[i] = 1
            pygame.mixer.Sound.set_volume(notefiles[i],100)
            t3 = threading.Thread(target=play_note, args=[i])
            t3.start()
        elif(buttonsPianoReading[i]) and not(newReading):
            buttonsPianoReading[i] = 0
            return
            


def updatePianoLed():
    for i in range(8):
        wiringpi.digitalWrite(ledPianoPin[i], buttonsPianoReading[i])


###################################################################################################################
startButtonPinLocation = 200
wiringpi.pinMode(startButtonPinLocation, 0)
ledoffset = 50

# Declaring button input as an i2C input
for i in range(4):
    for j in range(8):
        wiringpi.pinMode(buttonPinLocation[i][j], 0)
        wiringpi.pinMode(ledPinLocation[i][j], 1)


# Array for pressed or not pressed buttonsReading
buttonsReading = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
clickbeatInProgress = False


# Play single beats
def play_beat(row):
    audiofiles[row].play()
    time.sleep(1)
    return


def play_beat_diff_thread(row):
    t3 = threading.Thread(target=play_beat, args=[row])
    t3.start()
    return


def play_all_beats():
    for i in range(8):
        for j in range(4):
            if buttonsReading[j][i]:
                audiofiles[j].play()
        if i <7:
            time.sleep((beatsPause)/1000)
        # else:
        #     print('Hello')
    return

# Check for input and update the buttonsReading array  for BUTTONS


flagPressedState = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


def updateButtonsReading():
    global buttonsReading
    global flagPressedState
    for i in range(4):
        for j in range(8):
            newReading = wiringpi.digitalRead(buttonPinLocation[i][j])
            # print(buttonsReading)
            # if recent/prev is 0 then new/next is 1, meaning button get turned on
            if ((buttonsReading[i][j] == 0) and (newReading == 1) and flagPressedState[i][j] == 0):
                flagPressedState[i][j] = 1
                buttonsReading[i][j] = 1
                # threading
                t3 = threading.Thread(target=play_beat, args=[i])
                t3.start()

            elif ((buttonsReading[i][j] == 1) and (newReading == 0) and flagPressedState[i][j] == 1):
                # print("1,0,1")
                flagPressedState[i][j] = 0

            # if recent/prev is 1 then new/next is 1, meaning button get turned off
            elif (buttonsReading[i][j] == 1 and newReading == 1 and flagPressedState[i][j] == 0):
                flagPressedState[i][j] = 1
                buttonsReading[i][j] = 0

            elif (buttonsReading[i][j] == 0 and newReading == 0 and flagPressedState[i][j] == 1):
                flagPressedState[i][j] = 0

            # if same then skip
            else:
                pass
    return
# update the LED, if pressed then turns on, until it got pressed again ->then will turn off


def updateLed():
    for i in range(4):
        for j in range(8):
            wiringpi.digitalWrite(ledPinLocation[i][j], buttonsReading[i][j])
    return


def startButtonPressed():
    if(GPIO.input(4)):
        #print('Start button pressed')
        GPIO.output(17, GPIO.LOW)
        return True
    return GPIO.input(4)
    # return wiringpi.digitalRead(startButtonPinLocation)


def turnOffAll():
    global buttonsReading
    buttonsReading = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    for i in range(4):
        for j in range(8):
            wiringpi.digitalWrite(ledPinLocation[i][j], 0)
    return


def execute_beats():
    t = threading.Thread(target=sweepLED, args=[])
    t.start()
    play_all_beats()
    time.sleep(beatsPause/1000)
    #t.join()
    
    return


def sweepLED():
    for j in range(8):
        for i in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], buttonsReading[i][j])
        
        time.sleep((beatsPause-ledoffset)/1000)
        for i in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], 0)
    return


def inverseSweepLED():
    for j in range(8):
        for i in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], 1)
        time.sleep(beatsPause/1000)

        for i in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], buttonsReading[i][j])
    return


def checkStartButton(starttime):
    global stopButtonPressed
    stopButtonPressed = False
    while True:
        # if it is pressed then no need to change to False. Just wait until the next iteration
        if(stopButtonPressed):
            break
        timeNow = datetime.datetime.now()
        if(timeNow-starttime).seconds > minimumSec:
            stopButtonPressed = GPIO.input(4)
            #print("meow")
            if GPIO.input(4) == True:
                GPIO.output(17, GPIO.HIGH)
    return


def pauseAll():
    return


def executeClickbeat():
    global clickbeatInProgress
    clickbeatInProgress = True
    # print("triggered")
    starttime = datetime.datetime.now()

    # make a separate thread for checking stopButtonPressed
    t2 = threading.Thread(target=checkStartButton, args=[starttime])
    t2.start()

    # this loop will run forever until 1)exceed 5 mins 2)start/stop button pressed again
    while True:
        # check if it has been _ minutes, if exceed the limit then turns everything off.
        endtime = datetime.datetime.now()
        if (endtime-starttime).seconds > timeoutSec:
            turnOffAll()
            break
        if(stopButtonPressed):
            break
        execute_beats()
    clickbeatInProgress = False
    t2.join()

    # Check if start button pressed but if only time exceed minimum second elapsed (to atleast play some beats)

    # RESET LED -> TURN ONLY last saved array, STOP AUDIO, *DONT RESET ARR



while True:
    updateButtonsPianoReading()
    updatePianoLed()
    # print(stopButtonPressed)
    # print(buttonsReading)
    # print(startButtonPressed())
    # time.sleep(0.1)
    if not clickbeatInProgress:
        updateButtonsReading()
        updateLed()
    # if (startButtonPressed()):
        if (startButtonPressed()):
            #print("executed mainly")
            t1 = threading.Thread(target=executeClickbeat, args=[])
            # executeClickbeat()
            t1.start()
