import pygame
import time
import options
import pellet
from globvars import *

class Lightning(pellet.Pellet):
  def __init__(self, tank1, tank2):
    pellet.Pellet.__init__(self, tank1)
    self.weapon = 2
    self.enemy = tank2
    self.state = 'dead'
    self.duration = 0
    self.size = 65
    self.xposc = 0
    self.yposc = 0
    self.image = options.load_image('lightning_blue.png', self.size, self.size, transparent=True)
    self.rect = self.image.get_rect()

  def _shoot(self):
    pass

  def shoot(self):
    self.state = 'alive'
    self.rect.centerx = self.enemy.rect.centerx
    self.rect.centery = self.enemy.rect.centery
    soundLightning.play()

  def update(self, screen):
    """Update the time and visibility of the lightning weapon."""
    if self.state == 'alive' or self.state == 'stale':
      if self.duration == 50:
	self.duration = 0
	self.kill()
      self.rect.centerx = self.enemy.rect.centerx
      self.rect.centery = self.enemy.rect.centery
      self.duration += 1
