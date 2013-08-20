import pygame
from pygame.locals import *
import sys
from globvars import *


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


def controls(screen, backgroundRect):
  fontSize = 40
  offset = 30
  controlsFont = pygame.font.Font(None, fontSize)

  while 1:
    screen.fill(BLACK)
    controlsSurface = controlsFont.render('MISSION: The goal is to defeat your opponent by using items picked up.', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y))
    controlsSurface = controlsFont.render('First one to get to an item\'s location takes that item.', 1, WHITE)
    screen.blit(controlsSurface, (fontSize*3, backgroundRect.y+offset))
    offset += 50
    controlsSurface = controlsFont.render('CONTROL KEYS:', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('Top Player:', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('Navigate: mouse cursor', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('1st item: j, 2nd item: k, 3rd item: l', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('basic pellet fire: mouse click', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 50
    controlsSurface = controlsFont.render('Bottom Player:', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('Navigate: arrow keys', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('1st item: a, 2nd item: s, 3rd item: d', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    controlsSurface = controlsFont.render('basic pellet fire: spacebar', 1, WHITE)
    screen.blit(controlsSurface, (0, backgroundRect.y+offset))
    offset += 30
    offset = 30    # reset offset
    pygame.display.update()

    for e in pygame.event.get():
      if e.type == KEYDOWN:
        if e.key == K_ESCAPE or e.key == K_RETURN:
          return
