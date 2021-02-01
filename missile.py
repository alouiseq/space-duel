import pygame
from pygame.locals import *
from globvars import *
import pellet
import options
import math


class Missile(pellet.Pellet):
  def __init__(self, tank1, tank2):
    pellet.Pellet.__init__(self, tank1)
    self.weapon = 1
    self.enemy = tank2
    self.state = 'dead'
    self.speed = 3
    self.size = 35
    self.xposc = 0
    self.yposc = 0
    self.image = options.load_image('missile.png', self.size, self.size+20, 'top', 1)
    self.imageOrig = self.image

  def _shoot(self):
    pass

  def shoot(self):
    """Fire missiles with target tracking capability."""
    #print 'SHOOT MISSILE'
    self.rect.centerx = self.tank.rect.x + (self.tank.size / 2)
    if self.side == 'top':
      self.rect.centery = self.tank.rect.bottom
    if self.side == 'bottom':
      self.rect.centery = self.tank.rect.top

    self.state = 'alive'
    if self.side == 'top':
      self.yposc += self.speed
    if self.side == 'bottom':
      self.yposc -= self.speed
    soundMissile.play()
    
  def update(self):
    """Update the position of missiles and terminate out-of-bounds missiles."""
    if self.state == 'alive' or self.state == 'stale':
      if self.rect.centerx < self.enemy.rect.centerx:
  self.xposc = self.speed
      elif self.rect.centerx > self.enemy.rect.centerx:
  self.xposc = -self.speed
      else:    # ==
  self.xposc = 0
      if self.rect.centery < self.enemy.rect.centery:
  self.yposc = self.speed
      elif self.rect.centery > self.enemy.rect.centery:
  self.yposc = -self.speed
      else:    # ==
  self.yposc = 0

      self.rect.move_ip(self.xposc, self.yposc)
      #if self.side == 'top':
      self.image = options.rotate_image(self.imageOrig, math.degrees(math.atan2(self.xposc, self.yposc)))
      #if self.side == 'bottom':
      #	self.image = options.rotate_image(self.imageOrig, math.degrees(math.atan2(self.xposc, self.yposc)))
      if options.offEdges(self.rect):
  self.kill()
