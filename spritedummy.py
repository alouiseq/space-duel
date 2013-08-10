import pygame
import options
from globvars import *

"""Only use is to create a sprite."""
class Dummy(pygame.sprite.Sprite):
  def __init__(self, rect, radius):
    pygame.sprite.Sprite.__init__(self)
    self.rect = rect
    self.radius = radius

