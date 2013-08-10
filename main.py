import pygame
from pygame.locals import *
import sys
import random
import options
import machine
import pellet
import menu
from globvars import *
import missile
import lightning
import shield
import items
import spritedummy


def main():
  # initialize pygame and screen
  pygame.init()
  screen = pygame.display.set_mode((MAXWIDTH, MAXHEIGHT))
  pygame.display.set_caption('Dominance')
  rotatePlatform = 0    # count when to rotate platform
  angle = 0
  #xtemp = MAXWIDTH
  #ytemp = 
  # not game loop - loop for menu or start game over
  while 1:
    # blit background to screen
    #background = pygame.Surface(screen.get_size()).convert()
    xsize, ysize = screen.get_size()
    back = options.load_image('pyrobora.jpg', xsize, ysize)
    background = options.load_image('pyrobora.jpg', xsize, ysize)
    offset = 20
    backgroundRect = background.get_rect()
    backOrigCenter = backgroundRect.center
    screen.fill(BLACK)
 
    # introduce other platforms
    #nextPlat = options.load_image('earth.jpg', xtemp, ytemp)
    

    
    # game menu returns game mode: 1-single, 2-multi, 3-controls 
    mode = menu.game_menu(screen, backgroundRect)
    if mode == 1:
      playerType = 'Computer'
    elif mode == 2:
      playerType = 'Player2'

    # other initializations
    i = 1
    counter = 0
    countP1 = 0
    countP2 = 0
    damage_p1 = 100
    damage_p2 = 100
    goshotsP1 = False
    goshotsP2 = False
    activeP2 = False
    gameover = [False]
    mainClock = pygame.time.Clock()
    FPS = 60
    pygame.mouse.set_pos(backgroundRect.midtop)  # need for multiplayer mode
    pygame.mouse.set_visible(False)
    tempx = 0
    tempy = 0

    # initialize player objects
    player1 = machine.Machine(backgroundRect.midbottom, 'bottom')
    player2 = machine.Machine(backgroundRect.midtop, 'top', playerType)

    # initialize sprite groups
    players = pygame.sprite.RenderPlain(player1, player2)
    pellets_p1 = pygame.sprite.RenderPlain()
    pellets_p2 = pygame.sprite.RenderPlain()
    missiles_p1 = pygame.sprite.OrderedUpdates()
    missiles_p2 = pygame.sprite.OrderedUpdates()
    lightning_p1 = pygame.sprite.Group()
    lightning_p2 = pygame.sprite.Group()
    shield_p1 = pygame.sprite.GroupSingle()
    shield_p2 = pygame.sprite.GroupSingle()
    pickups = pygame.sprite.Group()
    itemsP1 = pygame.sprite.OrderedUpdates()
    itemsP2 = pygame.sprite.OrderedUpdates()

    # game loop
    while 1:
      # rotate platform
      rotatePlatform += 1
      #if (rotatePlatform % 101) == 0:
      angle += .20
      background = options.rotate_image(back, angle)
      backgroundRect = background.get_rect()
      backgroundRect.center = backOrigCenter

      counter += 1
      countP1 += 1
      countP2 += 1
      for event in pygame.event.get():
	if event.type == QUIT:
	  sys.exit()
	elif event.type == KEYDOWN:
	  if event.key == K_ESCAPE:
	    sys.exit()
	  elif event.key == K_LEFT:
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
          if event.key == K_a:
            if items.FREESLOTS1[0] == False:
              for item in itemsP1.sprites():
                if item.slot == 0:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
		        break
		  elif item.weapon == SHIELD:
                    if shield_p1.sprite:
                      shield_p1.sprite.timerStart = True
		  item.assignSlot(0, 'bottom')
		  itemsP1.remove(item)
          if event.key == K_s:
            if items.FREESLOTS1[1] == False:
              for item in itemsP1.sprites():
                if item.slot == 1:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == SHIELD:
                    if shield_p1.sprite:
                      shield_p1.sprite.timerStart = True
		  item.assignSlot(1, 'bottom')
		  itemsP1.remove(item)
          if event.key == K_d:
            if items.FREESLOTS1[2] == False:
              for item in itemsP1.sprites():
                if item.slot == 2:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p1.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == SHIELD:
                    if shield_p1.sprite:
                      shield_p1.sprite.timerStart = True
		  item.assignSlot(2, 'bottom')
		  itemsP1.remove(item)
          if event.key == K_j:
            if items.FREESLOTS2[0] == False:
              for item in itemsP2.sprites():
                if item.slot == 0:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
		        break
		  elif item.weapon == SHIELD:
                    if shield_p2.sprite:
                      shield_p2.sprite.timerStart = True
		  item.assignSlot(0, 'top')
		  itemsP2.remove(item)
          if event.key == K_k:
            if items.FREESLOTS2[1] == False:
              for item in itemsP2.sprites():
                if item.slot == 1:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == SHIELD:
                    if shield_p2.sprite:
                      shield_p2.sprite.timerStart = True
		  item.assignSlot(1, 'top')
		  itemsP2.remove(item)
          if event.key == K_l:
            if items.FREESLOTS2[2] == False:
              for item in itemsP2.sprites():
                if item.slot == 2:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == SHIELD:
                    if shield_p2.sprite:
                      shield_p2.sprite.timerStart = True
		  item.assignSlot(2, 'top')
		  itemsP2.remove(item)
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
          player2.xpos = event.pos[0] - player2.rect.centerx
          player2.ypos = event.pos[1] - player2.rect.centery
        if event.type == MOUSEBUTTONDOWN:
          goshotsP2 = True
          countP2 = 10
        elif event.type == MOUSEBUTTONUP:
          goshotsP2 = False

      if goshotsP1 and countP1 == 10:
	# ensure enough distance between bullets for visibility
	pellets_p1.add(pellet.Pellet(player1))
	countP1 = 0
      if goshotsP2 and countP2 == 10:
	pellets_p2.add(pellet.Pellet(player2))
	countP2 = 0

      # Artificial Intelligence
      if playerType == 'Computer':
        activeP2 = False
	if i == 50:
	  itemList = pickups.sprites()
          if not itemList:
            player2.itemSprite = None
            player2.ai(angle, MAXWIDTH/2-20, offset)
          else:  # pick up items are available
            for findItem in itemList:
              if findItem.side == 'top':
                player2.itemSprite = findItem
	  # randomize shooting
	  pick = random.randint(0,2)
          if pick == PELLETS:
	    pellets_p2.add(pellet.Pellet(player2))
          else:
	    if items.FREESLOTS2[pick] == False:
	      for item in itemsP2.sprites():
		if item.slot == pick:
		  if item.weapon == MISSILE:
		    for weapon in missiles_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == LIGHTNING:
		    for weapon in lightning_p2.sprites():
		      if weapon.state != 'stale':
			weapon.shoot()
			weapon.state = 'stale'
			break
		  elif item.weapon == SHIELD:
                    item.timerStart = True
		  item.assignSlot(pick, 'top')
		  itemsP2.remove(item)
	  i = 0
	i += 1
      elif playerType == 'Player2':
        activeP2 = True

      # randomize appearance of items on screen
      if counter == 100 and not pickups:
        choice = random.randint(0, 3)
        if choice:
          pickups.add(items.Items(choice, 'top', 1, angle, MAXWIDTH/2-20))
          pickups.add(items.Items(choice, 'bottom', 1, angle, MAXWIDTH/2-20))
      if counter == 100:
        counter = 0
      
      # collision with pellets (-1 damage)
      collidedwith_p1 = pygame.sprite.spritecollide(player1, pellets_p2, True)
      collidedwith_p2 = pygame.sprite.spritecollide(player2, pellets_p1, True)
      if not shield_p1.sprite:
        damage_p1 = damage_p1 - (len(collidedwith_p1))
      elif not shield_p1.sprite.timerStart:
        damage_p1 = damage_p1 - (len(collidedwith_p1))
      if not shield_p2.sprite:
        damage_p2 = damage_p2 - (len(collidedwith_p2))
      elif not shield_p2.sprite.timerStart:
        damage_p2 = damage_p2 - (len(collidedwith_p2))
      
      # collision with missiles  (-10 damage)
      collidedw_p1_missile = pygame.sprite.spritecollide(player1, missiles_p2, True)
      collidedw_p2_missile = pygame.sprite.spritecollide(player2, missiles_p1, True)
      if not shield_p1.sprite:
        damage_p1 = damage_p1 - (10 * len(collidedw_p1_missile))
      elif not shield_p1.sprite.timerStart:
        damage_p1 = damage_p1 - (10 * len(collidedw_p1_missile))
      if not shield_p2.sprite:
        damage_p2 = damage_p2 - (10 * len(collidedw_p2_missile))
      elif not shield_p2.sprite.timerStart:
        damage_p2 = damage_p2 - (10 * len(collidedw_p2_missile))

      # collision with lightning (-5 over time)
      collidedw_p1_lightning = pygame.sprite.spritecollide(player1, lightning_p2, False)
      collidedw_p2_lightning = pygame.sprite.spritecollide(player2, lightning_p1, False)
      if not shield_p1.sprite:
	damage_p1 = damage_p1 - (.5 * len(collidedw_p1_lightning))
      elif not shield_p1.sprite.timerStart:
        damage_p1 = damage_p1 - (.5 * len(collidedw_p1_lightning))
      if not shield_p2.sprite:
        damage_p2 = damage_p2 - (.5 * len(collidedw_p2_lightning))
      elif not shield_p2.sprite.timerStart:
        damage_p2 = damage_p2 - (.5 * len(collidedw_p2_lightning))

      # collision with weapon fires
      pygame.sprite.groupcollide(pellets_p1, missiles_p2, True, True)
      pygame.sprite.groupcollide(pellets_p2, missiles_p1, True, True)

      # collision with items
      collidedw_items = pygame.sprite.groupcollide(pickups, players, False, False)
      for item in collidedw_items.keys():
        pickups.empty()
	if item.side == 'top' and (len(itemsP2) <= 3):
	  i = 0
	  while (not items.FREESLOTS2[i]):
	    i += 1
	    if(i > 2):
	      break
	  if i <= 2:
	    item.equipped(i)
	    itemsP2.add(item)
          if item.weapon == MISSILE:
	    missiles_p2.add(missile.Missile(player2, player1))
          elif item.weapon == LIGHTNING:
	    lightning_p2.add(lightning.Lightning(player2, player1))
          elif item.weapon == SHIELD:
            shield_p2.add(shield.Shield(player2))
        elif item.side == 'bottom' and (len(itemsP1) <= 3):
	  i = 0
	  while (not items.FREESLOTS1[i]):
	    i += 1
	    if(i > 2):
	      break
	  if i <= 2:
	    item.equipped(i)
	    itemsP1.add(item)
          if item.weapon == MISSILE:
	    missiles_p1.add(missile.Missile(player1, player2))
          elif item.weapon == LIGHTNING:
	    lightning_p1.add(lightning.Lightning(player1, player2))
          elif item.weapon == SHIELD:
            shield_p1.add(shield.Shield(player1))
        break

      # damage allocations
      if damage_p1 < 0:
	player1.damage = 0 
      else:
        player1.damage = damage_p1
      if damage_p2 < 0:
      	player2.damage = 0
      else:
        player2.damage = damage_p2

      # circle's circumference used as boundaries
      circle = pygame.draw.circle(screen, GREEN, (backgroundRect.centerx, backgroundRect.centery), MAXWIDTH/2-20)
      circSprite = spritedummy.Dummy(circle, MAXWIDTH/2-20)
      if not pygame.sprite.collide_circle(circSprite, player1):
        player1.fall(screen)
      if not pygame.sprite.collide_circle(circSprite, player2) and playerType != 'Computer':
        player2.fall(screen)

      # set a border around player equipped items on screen
      item1rect = pygame.Rect(0, 0, ITEMSIZE, ITEMSIZE*3)
      item2rect = pygame.Rect(0, MAXHEIGHT/2, ITEMSIZE, ITEMSIZE*3)

      # blits
      screen.blit(background, backgroundRect)
      players.draw(screen) 
      pellets_p1.draw(screen)
      pellets_p2.draw(screen)

      if shield_p1.sprite:
        if shield_p1.sprite.timerStart:
          shield_p1.draw(screen)
      if shield_p2.sprite:
	if shield_p2.sprite.timerStart:
	  shield_p2.draw(screen)
      
      for each in missiles_p1:
	if each.state == 'alive' or each.state == 'stale':
	  screen.blit(each.image, each.rect)
      for each in lightning_p1:
	if each.state == 'alive' or each.state == 'stale':
	  screen.blit(each.image, each.rect)
      for each in missiles_p2:
	if each.state == 'alive' or each.state == 'stale':
	  screen.blit(each.image, each.rect)
      for each in lightning_p2:
	if each.state == 'alive' or each.state == 'stale':
	  screen.blit(each.image, each.rect)

      pygame.draw.rect
      pickups.draw(screen)
      pygame.draw.rect(screen, RED, item1rect, 1)
      pygame.draw.rect(screen, BLUE, item2rect, 1)
      itemsP1.draw(screen)
      itemsP2.draw(screen)
      options.display_keys(screen)

      # updates
      players.update(backgroundRect, screen, mode, gameover)
      pellets_p1.update()
      pellets_p2.update()
      missiles_p1.update()
      missiles_p2.update()
      lightning_p1.update(screen)
      lightning_p2.update(screen)
      shield_p1.update()
      shield_p2.update()

      pygame.mouse.set_pos(player2.rect.centerx, player2.rect.centery)
      pygame.display.update()
      mainClock.tick(FPS)

      # handle gameover
      if gameover[0]:
        players.empty()
        pellets_p1.empty()
        pellets_p2.empty()
	missiles_p1.empty()
	missiles_p2.empty()
	lightning_p1.empty()
	lightning_p2.empty()
        shield_p1.empty()
        shield_p2.empty()
	pickups.empty()
	itemsP1.empty()
	itemsP2.empty()
        gameover = False
	break


if __name__ == '__main__':
  main()
