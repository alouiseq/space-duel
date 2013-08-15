import pygame
from pygame.locals import *
import sys
import os
from globvars import *


def play_again():
  """Delay here until player selects to play or not."""
  delay = True
  while delay:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_RETURN:
          delay = False
        if event.key == K_ESCAPE:
          sys.exit()


def game_winner(side, screen, screen_rect, mode):
  """Display winning player on the screen.

  side: player side on screen
  screen: screen display
  screen_rect: screen's rectangle
  """
  if side == 'top':
    winner = 'Player 1'
    area = screen_rect.bottom - 100
  elif side == 'bottom':
    if mode == 1:   # single player mode
      winner = 'Computer'
    else:    # multiplayer mode
      winner = 'Player 2'
    area = screen_rect.top + 100
  fontSize = 80
  winner_font = pygame.font.Font(None, fontSize)
  winner_disp = winner_font.render(winner + ' wins!', 1,  WHITE)
  screen.blit(winner_disp, (screen_rect.centerx-(((fontSize/2)*len(winner))/2), screen_rect.centery-(fontSize/2)))
  pygame.display.update()
  play_again()


def load_image(image_file, xsize, ysize, side=None, transparent=False):
  """Load image from system file.

  image_file: file where image is stored
  xsize: width desired for image
  xsize: height desired for image
  side: side of player on screen
  Returns image surface.
  """
  dir_data = '/Users/aquiatchon/Dropbox/Projects/Dominance/images_sound'
  try:
    image_data = os.path.join(dir_data, image_file)
    imageinit = pygame.image.load(image_data)
    image = pygame.transform.scale(imageinit, (xsize, ysize))
    if side == 'top':
      image = pygame.transform.flip(image, 0, 1)
  except pygame.error, msg:
    print 'Cannot load the image: %s' % msg
    sys.exit()
    # raise SystemExit, msg
  if transparent:
    return image.convert_alpha()
  else:
    return image.convert()

def rotate_image(image, angle):
#def rotate_image(image, angle, screen):
  """Rotate image."""
  newImage = pygame.transform.rotate(image, angle)
  return newImage

def load_sound(sound_wav):
  """Load sound from system file.

  sound_wav: file where sound clip is stored
  Returns sound clip.
  """
  try:
    sound_dir = '/Users/aquiatchon/Dropbox/Projects/Dominance'
    sound_path = os.path.join(sound_dir, sound_wav)
    sound = pygame.mixer.Sound(sound_path)
  except pygame.error, msg:
    print 'Cannot load the sound clip: %s' % msg
    sys.exit()
    # raise SystemExit, msg
  return sound


def offEdges(bullet_rect):
  """Bullets from weapon go pass the edges of the screen will be removed.

  bullet_rect: rectangle of bullet to obtain x and y positions.
  Returns true if bullet goes pass the edges.
  """
  if (bullet_rect.left > MAXWIDTH or bullet_rect.right < 0 or
        bullet_rect.top > MAXHEIGHT or bullet_rect.bottom < 0):
    return True
  return False


def off_surface(player):
  """Prevents players from going past the game's surface."""
  if (player.rect.bottom > MAXWIDTH-20 or player.rect.bottom < 10 or
        player.rect.bottom > MAXHEIGHT-20 or player.rect.bottom < 10):
    return 0, 0


def display_keys(screen):
  fontSize = 20
  font = pygame.font.Font(None, fontSize)

  # handle top and bottom players
  # top
  key = font.render('j', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), ITEMSIZE-(ITEMSIZE-fontSize)))
  key = font.render('k', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), 2*(ITEMSIZE)-(ITEMSIZE-fontSize)))
  key = font.render('l', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), 3*(ITEMSIZE)-(ITEMSIZE-fontSize)))

  # bottom
  key = font.render('a', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), MAXHEIGHT/2 + ITEMSIZE-(ITEMSIZE-fontSize)))
  key = font.render('s', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), MAXHEIGHT/2 + 2*(ITEMSIZE)-(ITEMSIZE-fontSize)))
  key = font.render('d', 1,  WHITE)
  screen.blit(key, (ITEMSIZE-(ITEMSIZE-fontSize), MAXHEIGHT/2 + 3*(ITEMSIZE)-(ITEMSIZE-fontSize)))
