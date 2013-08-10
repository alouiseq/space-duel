import pygame
from pygame.locals import *
import sys
import os
import random

MAXWIDTH = 800
MAXHEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GAMEOVER = False


def game_menu(screen, backgroundRect):
  """Menu for user to select a game mode.

  screen: display surface
  backgroundRect: rectangle of background with size of screen
  Returns the game mode.
  """
  mode = 1   # game modes (1=singleplayer, 2=multiplayer, 3=controls)
  txtSize = 40

  # create text surfaces
  font = pygame.font.Font(None, txtSize)
  onePlayer_txt = 'SINGLE PLAYER'
  onePlayer = font.render(onePlayer_txt, 1, WHITE)
  oneRect = onePlayer.get_rect()
  oneRect.center = backgroundRect.center
  oneRect.top = oneRect.top - (txtSize + 10)
  twoPlayer_txt = 'MULTIPLAYER'
  twoPlayer = font.render(twoPlayer_txt, 1, WHITE)
  twoRect = twoPlayer.get_rect()
  twoRect.center = backgroundRect.center
  controls_txt = 'CONTROLS'
  controls = font.render(controls_txt, 1, WHITE)
  conRect = controls.get_rect()
  conRect.center = backgroundRect.center
  conRect.top = conRect.top + (txtSize + 10)

  # text surface for selected mode
  onePlayerSel = font.render(onePlayer_txt, 1, RED)
  twoPlayerSel = font.render(twoPlayer_txt, 1, RED)
  controlsSel = font.render(controls_txt, 1, RED)
  
  screen.fill(BLACK)

  while 1:
    xmouse, ymouse = pygame.mouse.get_pos()
    if oneRect.collidepoint(xmouse, ymouse):
      mode = 1
    if twoRect.collidepoint(xmouse, ymouse):
      mode = 2
    if conRect.collidepoint(xmouse, ymouse):
      mode = 3
    for event in pygame.event.get():
      if event.type == QUIT:
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        if event.key == K_DOWN:
          mode += 1
          if mode > 3:
            mode = 1
        if event.key == K_UP:
          mode -= 1
          if mode < 1:
            mode = 3
        if event.key == K_RETURN:
          return mode
      if event.type == MOUSEBUTTONDOWN:
        return mode
        

    screen.blit(onePlayer, oneRect)
    screen.blit(twoPlayer, twoRect)
    screen.blit(controls, conRect)

    if mode == 1:
      screen.blit(onePlayerSel, oneRect)
    elif mode == 2:
      screen.blit(twoPlayerSel, twoRect)
    elif mode == 3:
      screen.blit(controlsSel, conRect)
    
    pygame.display.update()


def play_again():
  """Delay here until player selects to play or not."""
  delay = True
  while delay:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        delay = False


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
  winner_font = pygame.font.Font(None, 80)
  winner_disp = winner_font.render(winner + ' wins!', 1,  WHITE)
  screen.blit(winner_disp, (screen_rect.left, area))
  pygame.display.update()
  play_again()


def loadImage(image_file, size, side=None):
  """Load image from system file.

  image_file: file where image is stored
  size: size desired for image
  side: side of player on screen
  Returns image surface.
  """
  dir_data = '/Users/aquiatchon/Dropbox/Projects/Dominance/images_sound'
  try:
    image_data = os.path.join(dir_data, image_file)
    imageinit = pygame.image.load(image_data)
    image = pygame.transform.scale(imageinit, (size, size))
    if side == 'top':
      image = pygame.transform.flip(image, 0, 1)
  except pygame.error, msg:
    print 'Cannot load the image: %s' % msg
    sys.exit()
    # raise SystemExit, msg
  return image.convert()


def loadSound(sound_wav):
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
    

class Tank(pygame.sprite.Sprite):
  def __init__(self, initpos, side, playerType='Player1'):
    pygame.sprite.Sprite.__init__(self)
    self.xpos = 0
    self.ypos = 0
    self.speed = 5
    self.size = 100
    self.state = 'still'
    self.direction = {'left':False, 'right':False, 'up':False, 'down':False}
    # screen texts
    self.text_font = pygame.font.Font(None, 20)
    self.damage_font = pygame.font.Font(None, 30)
    self.damage_surf = None
    self.damage = None
    #self.damage_font = pygame.font.Font(None, 40)
    self.player = playerType
    self.side = side
    if self.side == 'top':
      topleft = (initpos[0] - (self.size/2), initpos[1])
    elif self.side == 'bottom':
      topleft = (initpos[0] - (self.size/2), initpos[1] - self.size)
    self.text_player = self.text_font.render(self.player, 1, WHITE)
    # image & sound
    self.image = loadImage('tank.jpg', self.size, self.side)
    self.rect = self.image.get_rect()
    self.rect.topleft = topleft
    # sound = loadSound('changeme')

  def _text(self, screen):
    """Blitting player text and damage onto screen.

    screen: screen display
    """
    self.damage_surf = self.damage_font.render('%d' % self.damage, 1, RED)
    if self.side == 'top':
      screen.blit(self.text_player, (self.rect.left + (.20 * self.size), self.rect.top))
      screen.blit(self.damage_surf, ((self.rect.right - 15), (self.rect.top - 5)))
    if self.side == 'bottom':
      screen.blit(self.text_player, (self.rect.left + (.20 * self.size), self.rect.bottom - 13))
      screen.blit(self.damage_surf, ((self.rect.right - 15), (self.rect.bottom - 15)))

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
      
  def _boundaries(self, backgroundRect, side):
    """Stop player object from going pass the edges.

    backgroundRect:
    side:
    """
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > backgroundRect.right:
      self.rect.right = backgroundRect.right
    if self.side == 'top':
      if self.rect.top < 0:
	self.rect.top = 0
      if self.rect.bottom > MAXHEIGHT / 2:
	self.rect.bottom = MAXHEIGHT / 2
    elif self.side == 'bottom':
      if self.rect.top < MAXHEIGHT / 2:
	self.rect.top = MAXHEIGHT / 2
      if self.rect.bottom > MAXHEIGHT:
	self.rect.bottom = MAXHEIGHT

  def ai(self):
    """Artificial Intelligence that randomizes player's movements if player is computer."""
    moves = [self.move_left, self.move_right, self.move_up, self.move_down]
    moveChoice = random.randint(0, 3)
    for stopMove in range(0,4):
      if stopMove != moveChoice:
	moves[stopMove]('still') 
    moves[moveChoice]('moving')
    
  def update(self, backgroundRect, screen, mode):
    """Update the position of players and draw texts."""
    global GAMEOVER
    self.rect.move_ip(self.xpos, self.ypos)
    self._boundaries(backgroundRect, self.side)
    self._text(screen)      # draw players text 
    # tank destroyed
    if self.damage <= 0:
      self.state = 'destroyed'
      GAMEOVER = True
      game_winner(self.side, screen, screen.get_rect(), mode)


class Pellet(pygame.sprite.Sprite):
  def __init__(self, tank):
    pygame.sprite.Sprite.__init__(self)
    self.speed = 7
    self.size = 30
    self.side = tank.side
    self.yposc = 0
    self.xposc = 0
    self.status = 'alive'
    self.image = loadImage('bullet_small.png', self.size, self.side)
    self.rect = self.image.get_rect()
    #self.rect = self.rect.inflate(-(.5 * self.size), -(.5 * self.size))
    self.sound = loadSound('gunshot.wav')
    self.sound.play()
    self.rect.centerx = tank.rect.x + (tank.size / 2)
    if self.side == 'top':
      self.rect.centery = tank.rect.bottom
    if self.side == 'bottom':
      self.rect.centery = tank.rect.top
    self._shoot()

  def _shoot(self):
    """Activate and fire the bullets out from the tank towards the enemy."""
    if self.side == 'top':
      self.yposc += self.speed
    if self.side == 'bottom':
      self.yposc -= self.speed

  def update(self):
    """Update the position of bullets and terminate out-of-bounds bullets."""
    self.rect.move_ip(self.xposc, self.yposc)
    if offEdges(self.rect):
      self.status = 'dead'
      self.kill()


def main():
  # other definitions
  global GAMEOVER

  # initialize pygame and screen
  pygame.init()
  screen = pygame.display.set_mode((MAXWIDTH, MAXHEIGHT))
  pygame.display.set_caption('Dominance')

  # not game loop - loop for menu or start game over
  while 1:
    # blit background to screen
    background = pygame.Surface(screen.get_size()).convert()
    backgroundRect = background.get_rect()
    screen.fill(BLACK)
    
    # game menu returns game mode: 1-single, 2-multi, 3-controls 
    mode = game_menu(screen, backgroundRect)
    if mode == 1:
      playerType = 'Computer'
    elif mode == 2:
      playerType = 'Player2'

    # other initializations
    i = 1
    countP1 = 0
    countP2 = 0
    damage_p1 = 100
    damage_p2 = 100
    goshotsP1 = False
    goshotsP2 = False
    activeP2 = False
    GAMEOVER = False
    mainClock = pygame.time.Clock()
    FPS = 60
    pygame.mouse.set_pos(backgroundRect.midtop)  # need for multiplayer mode
    pygame.mouse.set_visible(False)

    # initialize game objects
    player1 = Tank(backgroundRect.midbottom, 'bottom')
    player2 = Tank(backgroundRect.midtop, 'top', playerType)

    # initialize sprites
    players = pygame.sprite.RenderPlain(player1, player2)
    pellets_p1 = pygame.sprite.RenderPlain()
    pellets_p2 = pygame.sprite.RenderPlain()

    player_list = players.sprites()

    # game loop
    while 1:
      countP1 += 1
      countP2 += 1
      for event in pygame.event.get():
	if event.type == QUIT:
	  sys.exit()
	elif event.type == KEYDOWN:
	  if event.key == K_ESCAPE:
	    sys.exit()
	  elif event.key == K_LEFT:
            print 'test'
	    player1.move_left('moving')
	  elif event.key == K_RIGHT:
	    player1.move_right('moving')
	  elif event.key == K_UP:
	    player1.move_up('moving')
	  elif event.key == K_DOWN:
	    player1.move_down('moving')
	  elif event.key == K_SPACE:
	    goshotsP1 = True
	    countP1 = 10
	elif event.type == KEYUP:
	  if event.key == K_LEFT:
	    player1.move_left('still')
	  elif event.key == K_RIGHT:
	    player1.move_right('still')
	  elif event.key == K_UP:
	    player1.move_up('still')
	  elif event.key == K_DOWN:
	    player1.move_down('still')
	  elif event.key == K_SPACE:
	    goshotsP1 = False
        if event.type == MOUSEMOTION and activeP2:
          #(x, y) = pygame.mouse.get_pos()
          #print 'mouse: ', (x, y)
          #print 'player center ', player2.rect.center
          player2.xpos = event.pos[0] - player2.rect.centerx
          player2.ypos = event.pos[1] - player2.rect.centery
        if event.type == MOUSEBUTTONDOWN:
          goshotsP2 = True
          countP2 = 10
        elif event.type == MOUSEBUTTONUP:
          goshotsP2 = False


      if goshotsP1 and countP1 == 10:
	# ensure enough distance between bullets for visibility
	pellets_p1.add(Pellet(player1))
	countP1 = 0
      if goshotsP2 and countP2 == 10:
	pellets_p2.add(Pellet(player2))
	countP2 = 0

      if playerType == 'Computer':
        activeP2 = False
	# Artificial Intelligence
	if i ==50:
	  # AI moves with time delay
	  player2.ai()
	  # randomize shooting
	  wait = random.randint(0,1)
	  if wait:
	    pellets_p2.add(Pellet(player2))
	  i = 0
	i += 1
      elif playerType == 'Player2':
        activeP2 = True

      # collision detection
      collidedwith_p1 = []
      collidedwith_p2 = []
      collidedwith_p1 = pygame.sprite.spritecollide(player1, pellets_p2, True)
      collidedwith_p2 = pygame.sprite.spritecollide(player2, pellets_p1, True)
      damage_p1 = damage_p1 - (5 * len(collidedwith_p1))
      damage_p2 = damage_p2 - (5 * len(collidedwith_p2))
      player1.damage = damage_p1
      player2.damage = damage_p2

      # blits and updates 
      #screen.blit(background, backgroundRect)
      #screen.fill(WHITE)
      screen.fill(BLACK)
      players.draw(screen) 
      pellets_p1.draw(screen)
      pellets_p2.draw(screen)
      players.update(backgroundRect, screen, mode)
      pellets_p1.update()
      pellets_p2.update()
      #print pellets

      pygame.mouse.set_pos(player2.rect.centerx, player2.rect.centery)

      pygame.display.update()
      mainClock.tick(FPS)

      if GAMEOVER:
        players.empty()
        pellets_p1.empty()
        pellets_p2.empty()
        GAMEOVER = False
	break


if __name__ == '__main__':
  main()
