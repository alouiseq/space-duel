"""Global variables needed for game."""

import pygame
import sys

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAXWIDTH = 1000
MAXHEIGHT = 1000
ITEMSIZE = 30

MISSILE = 1
LIGHTNING = 2
SHIELD = 3
PELLETS = 4

# SOUNDS CLIPS
dir_data = 'images_sound/sounds/'
try:
  soundMove = pygame.mixer.Sound(dir_data+'movements.wav')
  soundPickup = pygame.mixer.Sound(dir_data+'pickup.wav')
  soundDamageHit = pygame.mixer.Sound(dir_data+'damage_hits.wav')
  soundPellet = pygame.mixer.Sound(dir_data+'pellets.wav')
  soundMissile = pygame.mixer.Sound(dir_data+'missile.wav')
  soundLightning = pygame.mixer.Sound(dir_data+'lightning.wav')
  soundShield = pygame.mixer.Sound(dir_data+'shield.wav')
  soundWin = pygame.mixer.Sound(dir_data+'flawless_victory.wav')
except pygame.error, msg:
  print 'Cannot load the sound: %s' % msg
  sys.exit()
