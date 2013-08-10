import pygame
import random
import math
import time
import options
from globvars import *


class Machine(pygame.sprite.Sprite):
  def __init__(self, initpos, side, playerType='Player1', angle=None):
    pygame.sprite.Sprite.__init__(self)
    self.xpos = 0
    self.ypos = 0
    self.speed = 6
    self.size = 50
    self.state = 'still'
    self.angleDeg = angle
    self.direction = {'left':False, 'right':False, 'up':False, 'down':False}
    # screen texts
    self.text_font = pygame.font.Font(None, 20)
    self.damage_font = pygame.font.Font(None, 30)
    self.damage_surf = None
    self.damage = 100
    self.player = playerType
    self.side = side
    self.gone = False     # when player falls out of of range
    self.angle = 0        # angle associated with out-of-range player
    self.itemSprite = None
    if self.side == 'top':
      topleft = (initpos[0] - (self.size/2), initpos[1])
      self.image = options.load_image('guard_front_flat.png', self.size, self.size+20, transparent=True)
    elif self.side == 'bottom':
      topleft = (initpos[0] - (self.size/2), initpos[1] - self.size-60)
      self.image = options.load_image('guard_back_flat.png', self.size, self.size+20, transparent=True)
    self.text_player = self.text_font.render(self.player, 1, WHITE)
    # image & sound
    self.rect = self.image.get_rect()
    #self.circle = pygame.draw.circle(self.image, GREEN, (self.rect.centerx, self.rect.centery), self.size/2)
    self.radius = self.size/2
    self.rect.topleft = topleft
    self.index = 0
    self.lefts = ['guard_left_leftup.png', 'guard_left_leftdown.png', 'guard_left_rightup.png', 'guard_left_flat.png'] 
    self.rights = ['guard_right_rightup.png', 'guard_right_rightdown.png', 'guard_right_leftup.png', 'guard_right_flat.png'] 
    self.downs = ['guard_front_leftup.png', 'guard_front_flat.png', 'guard_front_rightup.png', 'guard_front_flat.png']
    self.ups = ['guard_back_leftup.png', 'guard_back_flat.png', 'guard_back_rightup.png', 'guard_back_flat.png']
    # sound = options.load_sound('changeme')

  def _text(self, screen):
    """Blitting player text and damage onto screen.

    screen: screen display
    """
    # blit health bars
    emptyBar = options.load_image('Emptybar.png', 100, 50)
    if self.side == 'top':
      screen.blit(self.text_player, (50, 10))
      p2health = options.load_image('Redbar.png', int(self.damage), 50)
      screen.blit(emptyBar, (120, 0))
      screen.blit(p2health, (120, 0))
    if self.side == 'bottom':
      screen.blit(self.text_player, (50, MAXHEIGHT-40))
      p1health = options.load_image('Greenbar.png', int(self.damage), 50)
      screen.blit(emptyBar, (120, MAXHEIGHT-50))
      screen.blit(p1health, (120, MAXHEIGHT-50))

  def move_left(self, state):
    """Set the player's left movement based on user events.

    state: state player is currently in
    """
    self.state = state
    self.xpos = 0
    if self.state == 'still':
      self.direction['left'] = False
      if self.direction['right']:
        self.xpos += self.speed
    else:
      self.direction['left'] = True
      self.xpos -= self.speed
      if self.index > 3:
        self.index = 0
      self.image = options.load_image(self.lefts[self.index], self.size, self.size+20, transparent=True)
      self.index += 1

  def move_right(self, state):
    """Set the player's right movement based on user events.

    state: state player is currently in
    """
    self.state = state
    self.xpos = 0
    if self.state == 'still':
      self.direction['right'] = False
      if self.direction['left']:
        self.xpos -= self.speed
    else:
      self.direction['right'] = True
      self.xpos += self.speed
      if self.index > 3:
        self.index = 0
      self.image = options.load_image(self.rights[self.index], self.size, self.size+20, transparent=True)
      self.index += 1

  def move_up(self, state):
    """Set the player's up movement based on user events.

    state: state player is currently in
    """
    self.state = state
    self.ypos = 0
    if self.state == 'still':
      self.direction['up'] = False
      if self.direction['down']:
        self.ypos += self.speed
    else:
      self.direction['up'] = True
      self.ypos -= self.speed
      if self.index > 3:
        self.index = 0
      self.image = options.load_image(self.ups[self.index], self.size, self.size+20, transparent=True)
      self.index += 1

  def move_down(self, state):
    """Set the player's down movement based on user events.

    state: state player is currently in
    """
    self.state = state
    self.ypos = 0
    if self.state == 'still':
      self.direction['down'] = False
      if self.direction['up']:
        self.ypos -= self.speed
    else:
      self.direction['down'] = True
      self.ypos += self.speed
      if self.index > 3:
        self.index = 0
      self.image = options.load_image(self.downs[self.index], self.size, self.size+20, transparent=True)
      self.index += 1
      
  def _boundaries(self, side, offset=0):
    """Stop player object from going pass the edges.

    side: player side on the screen
    offset: offset between window edge and platform edge

    Note the xy coordinate placements and don't depend on the center of screen.
    side:
    """
    if self.player == 'Computer':
      radius = MAXWIDTH/2 - offset
      # x coordinates
      if self.rect.centerx > MAXWIDTH/2:
        x = self.rect.centerx - MAXWIDTH/2
      else:
        x = -(MAXWIDTH/2 - self.rect.centerx)
      # y coordinates
      if self.rect.bottom >= MAXHEIGHT/2:
        y = 0
      else:
        y = MAXHEIGHT/2 - self.rect.bottom
      
      # platform as a circle
      angleRad = math.atan2(y, x)
      self.x = radius * math.cos(angleRad)   # extremity
      self.y = radius * math.sin(angleRad)   # extremity
      
      # handle out-of-bounds
      adjust = 20
      xOutofBounds = False
      if ((self.rect.centerx < MAXWIDTH/2) and (self.rect.centerx < (MAXWIDTH/2 + self.x + adjust))):
        xOutofBounds = True
      elif ((self.rect.centerx > MAXWIDTH/2) and (self.rect.centerx > (MAXWIDTH/2 + self.x - adjust))):
        adjust = -adjust
        xOutofBounds = True
      if xOutofBounds:
	if self.rect.bottom > MAXHEIGHT/2:
	  self.rect.bottom = MAXHEIGHT/2
	else:
	  if self.rect.bottom < MAXHEIGHT/2 - self.y + math.fabs(adjust):
            #print 'LEFT QUAD:', self.rect.centerx, self.x, 'diff:', 500+self.x + adjust
            #print 'DOWN QUAD: ', self.rect.bottom, self.y, 'diff:', 500-self.y + math.fabs(adjust)
	    self.rect.centerx = MAXWIDTH/2 + self.x + adjust
	    self.rect.bottom = MAXHEIGHT/2 - self.y + math.fabs(adjust)
        xOutofBounds = False
      else:   # handle top player going pass the players' interface boundary
        if self.rect.bottom > MAXHEIGHT/2:
          self.rect.bottom = MAXHEIGHT/2
        elif self.rect.bottom < adjust:
          self.rect.bottom = adjust
    else:
      if self.rect.left < 0:
	self.rect.left = 0
      if self.rect.right > MAXWIDTH:
	self.rect.right = MAXWIDTH
      if self.side == 'top':
	if self.rect.bottom < 0:
	  self.rect.bottom = 0
	if self.rect.bottom > MAXHEIGHT / 2:
	  self.rect.bottom = MAXHEIGHT / 2
      elif self.side == 'bottom':
	if self.rect.top < MAXHEIGHT / 2:
	  self.rect.top = MAXHEIGHT / 2
	if self.rect.bottom > MAXHEIGHT:
	  self.rect.bottom = MAXHEIGHT

  def fall(self, screen):
    """Instant death of player.

    screen: game screen
    """
    self.gone = True
    self.size -= 5
    self.angle += 40
    self.image = options.load_image('guard_front_flat.png', self.size, self.size, transparent=True)
    self.image = options.rotate_image(self.image, self.angle)
    # move dead player into space
    if self.rect.centerx > MAXWIDTH/2:
      self.rect.x = self.rect.x + 10
    elif self.rect.centerx < MAXWIDTH/2:
      self.rect.x = self.rect.x - 10
    if self.angle >= 360:
      self.gone = False
      self.damage = 0

  def ai(self, angle, speed, offset):
    """Artificial Intelligence that randomizes player's movements if player is computer.

    offset: account for space between platform and game window dimensions
    """
    moves = [self.move_left, self.move_right, self.move_up, self.move_down]
    moveChoice = random.randint(0, 3)
    for stopMove in range(0,4):
      if stopMove != moveChoice:
	moves[stopMove]('still') 
    moves[moveChoice]('moving')
    self._boundaries(self.side, offset)
    
  def update(self, backgroundRect, screen, mode, gameover):
    """Update the position of players and draw texts.

    backgroundRect: background rectangle
    screen: window screen
    mode: game mode
    gameover: flag if game has ended
    """
    if self.gone:
      pass
    else:
      if self.itemSprite:
	if self.rect.centerx < self.itemSprite.rect.centerx:
	  self.xpos = self.speed
	elif self.rect.centerx > self.itemSprite.rect.centerx:
	  self.xpos = -self.speed
	else:    # ==
	  self.xpos = 0
	if self.rect.centery < self.itemSprite.rect.centery:
	  self.ypos = self.speed
	elif self.rect.centery > self.itemSprite.rect.centery:
	  self.ypos = -self.speed
	else:    # ==
	  self.ypos = 0

      self.rect.move_ip(self.xpos, self.ypos)

      # check direction of movement to correspond with image movements
      if self.index > 3:
	self.index = 0
      if self.xpos < 0:
	self.image = options.load_image(self.lefts[self.index], self.size, self.size+20, transparent=True)
      if self.xpos > 0:
	self.image = options.load_image(self.rights[self.index], self.size, self.size+20, transparent=True)
      if self.ypos < 0:
	self.image = options.load_image(self.ups[self.index], self.size, self.size+20, transparent=True)
      if self.ypos > 0:
	self.image = options.load_image(self.downs[self.index], self.size, self.size+20, transparent=True)
      self.index += 1

      self._boundaries(self.side)
      self._text(screen)      # draw players text 
      # machine destroyed
      if self.damage <= 0:
	self.state = 'destroyed'
	gameover[0] = True
	options.game_winner(self.side, screen, screen.get_rect(), mode)

