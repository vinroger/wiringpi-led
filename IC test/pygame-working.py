import pygame
import time

# pygame.mixer.init()
# pygame.mixer.Channel(0).play(pygame.mixer.Sound('wav\crash.wav'))
# pygame.mixer.Channel(1).play(pygame.mixer.Sound('wav\kick.wav'))

pygame.mixer.init()
# Load two sounds
crash = pygame.mixer.Sound('wav\crash.wav')
kick = pygame.mixer.Sound('wav\kick.wav')
snare = pygame.mixer.Sound('wav\snare.wav')
hihat = pygame.mixer.Sound('wav\hihat.wav')
audiofiles = [crash, kick, snare, hihat]

buttonsReading = [
    [1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 1, 0],
    [1, 1, 0, 1, 1, 0, 1, 1]
]
# crash.play()
# time.sleep(1)


for i in range(8):
    for j in range(4):
        if buttonsReading[j][i]:
            audiofiles[j].play()
    time.sleep(0.2)
time.sleep(1)


# play(crash)
# time.sleep(1)

# t1 = threading.Thread(target=play, args=[crash])
# t1.start()
# play(kick)
# t1.join()
