import wiringpi as wiringpi
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import copy
import os
import datetime
import time
import threading
#import time

pin_base = 65       # lowest available starting number is 65
ic1_addr = 0x20     # A0, A1, A2 pins all wired to GND
ic2_addr = 0x21     # A0, A1, A2 pins all wired to GND
ic3_addr = 0x22     # A0, A1, A2 pins all wired to GND


buttonPinLocation = [
    [65, 66, 67, 68, 69, 70, 71, 72],
    [73, 74, 75, 76, 77, 78, 79, 80],
    [81, 82, 83, 84, 85, 86, 87, 88],
    [89, 90, 91, 92, 93, 94, 95, 96]
]

ledPinLocation = [
    [97, 98, 99, 100, 101, 102, 103, 104],
    [105, 106, 107, 108, 109, 110, 111, 112],
    [113, 114, 115, 116, 117, 118, 119, 120],
    [120, 121, 122, 123, 124, 125, 126, 127]
]

startButtonPinLocation = 128
wiringpi.pinMode(startButtonPinLocation, 0)

# DECLARATION of wiring Pi
wiringpi.wiringPiSetup()                    # initialise wiringpi
wiringpi.mcp23017Setup(pin_base, ic1_addr)
wiringpi.mcp23017Setup(82, ic2_addr)
wiringpi.mcp23017Setup(98, ic3_addr)
wiringpi.mcp23017Setup(115, ic3_addr)

# Declaring button input as an i2C input
for i in range(4):
    for j in range(8):
        wiringpi.pinMode(buttonPinLocation[i][j], 0)

# Declaring audio files wav etc
crash = AudioSegment.from_wav("wav/crash.wav")
hihat = AudioSegment.from_wav("wav/hihat.wav")
kick = AudioSegment.from_wav("wav/kick.wav")
snare = AudioSegment.from_wav("wav/snare.wav")

wavdict = {}
for i in ["0", "1"]:
    for j in ["0", "1"]:
        for k in ["0", "1"]:
            for l in ["0", "1"]:
                wavdict[i+j+k +
                        l] = AudioSegment.from_wav("combined/{}.wav".format(i+j+k+l))

# Declaring misc variables
timeoutSec = 300
# to avoid start button being pressed again and turns everything off,
# we set a timeout to atleast play some beats loop before the user can turn off the beats by pressing the start button again
minimumSec = 2
beatsPause = 400
stopButtonPressed = False

# Array for pressed or not pressed buttonsReading
buttonsReading = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


# Play single beats
def play_beats(row):
    if (row == 0):
        play(crash)
    elif (row == 1):
        play(hihat)
    elif (row == 2):
        play(kick)
    elif (row == 3):
        play(snare)

# Check for input and update the buttonsReading array  for BUTTONS


def updateButtonsReading():
    global buttonsReading
    for i in range(4):
        for j in range(8):
            newReading = wiringpi.digitalRead(buttonPinLocation[i][j])
            recentReading = buttonsReading[i][j]

            # if recent/prev is 0 then new/next is 1, meaning button get turned on
            if (recentReading == 0 and newReading == 1):
                buttonsReading[i][j] = 1
                play_beats(i)

            # if recent/prev is 1 then new/next is 0, meaning button get turned off
            elif (recentReading == 1 and newReading == 0):
                buttonsReading[i][j] = 0
                play_beats(i)

            # if same then skip
            else:
                pass


# update the LED, if pressed then turns on, until it got pressed again ->then will turn off
def updateLed():
    for i in range(4):
        for i in range(8):
            wiringpi.digitalWrite(ledPinLocation[i][j], buttonsReading[i][j])


def startButtonPressed():
    return wiringpi.digitalRead(startButtonPinLocation)


def turnOffAll():
    global buttonsReading
    buttonsReading = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    for i in range(4):
        for i in range(8):
            wiringpi.digitalWrite(ledPinLocation[i][j], 0)


def compile_audio():
    silence = AudioSegment.silent(duration=beatsPause*9, frame_rate=44100)
    # loop through frames in the array, create an audio, overlay it to silent(nothing inside) -> an audio to play
    for j in range(8):
        frame_str = ""
        for i in range(4):
            frame_str += str(buttonsReading[i][j])

        # string in each frame will look like something : frame_str="0011"
        audiofile = wavdict[frame_str]
        silence = silence.overlay(audiofile, position=beatsPause*(j+1))

    return silence


def play_beats(audio):
    t = threading.Thread(target=sweepLED, args=[])
    t.start()
    play(audio)
    t.join()


def sweepLED():
    for i in range(8):
        for j in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], buttonsReading[i][j])
        time.sleep(beatsPause/1000)
        for j in range(4):
            wiringpi.digitalWrite(ledPinLocation[i][j], 0)


def checkStartButton(starttime):
    global stopButtonPressed
    stopButtonPressed = False
    while True:
        # if it is pressed then no need to change to False. Just wait until the next iteration
        if(stopButtonPressed):
            break
        timeNow = datetime.datetime.now()
        if(timeNow-starttime).seconds > minimumSec:
            stopButtonPressed = wiringpi.digitalRead(startButtonPinLocation)


def pauseAll():
    return


while True:
    updateButtonsReading()
    updateLed()
    if (startButtonPressed()):
        starttime = datetime.datetime.now()

        # make a separate thread for checking stopButtonPressed
        t2 = threading.Thread(target=checkStartButton, args=[starttime])
        t2.start()
        compiledAudio = compile_audio()

        # this loop will run forever until 1)exceed 5 mins 2)start/stop button pressed again
        while True:
            # check if it has been _ minutes, if exceed the limit then turns everything off.
            endtime = datetime.datetime.now()
            if (endtime-starttime).seconds > timeoutSec:
                turnOffAll()
                break
            if(stopButtonPressed):
                break
            play_beats(compiledAudio)

        t2.join()

        # Check if start button pressed but if only time exceed minimum second elapsed (to atleast play some beats)

        # RESET LED -> TURN ONLY last saved array, STOP AUDIO, *DONT RESET ARR
