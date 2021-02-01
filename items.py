import pygame
import random
import math
import options
from globvars import *

# Slots that can carry up to 3 weapons
FREESLOTS1 = [True, True, True]
FREESLOTS2 = [True, True, True]

class Items(pygame.sprite.Sprite):
  def __init__(self, choice, side, assign=False, angle=0, radius=0):
    pygame.sprite.Sprite.__init__(self)
    self.weapon = choice
    self.side = side
    self.slot = 0
    self.size = ITEMSIZE
    self.x = 0
    self.y = 0
    self.angleDeg = angle
    self.speed = radius
    self.fire = None
    self.image = None
    self.rect = None
    if assign:
      self._assign_type()

  def _assign_type(self):
    if self.weapon == MISSILE:
      self.fire = 'missileIcon.jpg'
    elif self.weapon == LIGHTNING:
      self.fire = 'lightning-blue-1.png'
    elif self.weapon == SHIELD:
      self.fire = 'shield.png'
    self._randomizer()

  def _randomizer(self):
    """Randomly set x and y coordinates within the boundaries of a given platform."""
    angleRad = math.radians(self.angleDeg)
    self.x = self.speed * math.cos(angleRad)
    self.x = int(self.x)
    self.y = self.speed * math.sin(angleRad)
    self.y = int(self.y)
    if self.x < 0:
      self.x = random.randint(self.x + MAXWIDTH/2, MAXWIDTH/2 - self.x)
    else:
      self.x = random.randint(MAXWIDTH/2 - self.x, MAXWIDTH/2 + self.x)
    if self.side == 'top':
      if self.y < 0:
        self.y = random.randint(MAXHEIGHT/2 + self.y, (MAXHEIGHT/2) - self.size)
      elif self.y > 0:
        self.y = random.randint(MAXHEIGHT/2 - self.y, (MAXHEIGHT/2) - self.size)
      else:   # == 0
        self.y = MAXHEIGHT/2 - self.size
    elif self.side == 'bottom':
      if self.y <= 0:
        self.y = random.randint(MAXHEIGHT/2, MAXHEIGHT/2 - self.y)
      else:
        self.y = random.randint(MAXHEIGHT/2, MAXHEIGHT/2 + self.y)
      
    self.image = options.load_image(self.fire, self.size, self.size, 'top')
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y

  def equipped(self, slot):
    """Place player's weapon item on upper left corner of their screen (3 items maximum store)."""
    self.slot = slot;
    self.rect.x = 0
    if self.slot == 0:
      if self.side == 'top':
        FREESLOTS2[0] = False
  self.rect.y = 0 
      elif self.side == 'bottom':
        FREESLOTS1[0] = False
  self.rect.y = MAXHEIGHT/2
    if self.slot == 1:
      if self.side == 'top':
        FREESLOTS2[1] = False
  self.rect.y = self.size 
      elif self.side == 'bottom':
        FREESLOTS1[1] = False
  self.rect.y = MAXHEIGHT/2 + self.size
    if self.slot == 2:
      if self.side == 'top':
        FREESLOTS2[2] = False
  self.rect.y = self.size * 2 
      elif self.side == 'bottom':
        FREESLOTS1[2] = False
  self.rect.y = MAXHEIGHT/2 + (self.size * 2)

  def assignSlot(self, index, player):
    if player == 'top':
      FREESLOTS2[index] = True
    elif player == 'bottom':
      FREESLOTS1[index] = True
