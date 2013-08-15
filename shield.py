import pygame
from pygame.locals import *
import pellet
import options


class Shield(pygame.sprite.Sprite):
  def __init__(self, tank):
    pygame.sprite.Sprite.__init__(self)
    self.tank = tank
    self.weapon = 4
    self.timerStart = False
    self.time = 0
    self.size = tank.size + 40
    self.image = options.load_image('barrier.png', self.size, self.size, transparent=True)
    self.rect = self.image.get_rect()
    self.rect.centerx = self.tank.rect.centerx
    self.rect.centery = self.tank.rect.centery + 13

  def update(self):
    """Update the position of the shield as tank moves."""
    if self.timerStart:
      self.rect.centerx = self.tank.rect.centerx
      self.rect.centery = self.tank.rect.centery + 13
      if self.time > 200:
        self.kill()
      self.time += 1
