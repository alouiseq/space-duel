import pygame
import options
from globvars import *


class Pellet(pygame.sprite.Sprite):
  def __init__(self, tank):
    pygame.sprite.Sprite.__init__(self)
    self.tank = tank
    self.side = tank.side
    self.speed = 7
    self.size = 30
    self.yposc = 0
    self.xposc = 0
    self.status = 'alive'
    self.image = options.load_image('bullet.png', self.size, self.size, self.side, transparent=True)
    self.rect = self.image.get_rect()
    #self.rect = self.rect.inflate(-(.5 * self.size), -(.5 * self.size))
    self.sound = options.load_sound('gunshot.wav')
    self.rect.centerx = tank.rect.x + (tank.size / 2)
    if self.side == 'top':
      self.rect.centery = tank.rect.bottom
    if self.side == 'bottom':
      self.rect.centery = tank.rect.top
    self._shoot()

  def _shoot(self):
    """Activate and fire the bullets out from the tank towards the enemy."""
    #print 'SHOOT BULLET'
    if self.side == 'top':
      self.yposc += self.speed
    if self.side == 'bottom':
      self.yposc -= self.speed
    soundPellet.play()

  def update(self):
    """Update the position of bullets and terminate out-of-bounds bullets."""
    self.rect.move_ip(self.xposc, self.yposc)
    if options.offEdges(self.rect):
      self.status = 'dead'
      self.kill()
