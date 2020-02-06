import pygame
import time
import sys
import math
import random
from pygame.locals import *
from Class_Button import button

# update log
UpdateLog = '''
Aircraft Battle by AbsoCube Studio
Aircraft Battle Version2 Update Log:
Update Time : 2019/11/29 Friday
Update Contents:
    1. Fixed a BUG where the game could not be replayed.
    2. Fixed a BUG that could not be initialized when replaying the game.
Have a good game experience :)
'''
print(UpdateLog)

# ready
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Aircraft Battle by AbsoCube Studio     Version2")
icon = pygame.image.load("repository/spaceship.ico")
pygame.display.set_icon(icon)
AC = pygame.image.load("repository/AbsoCube.jpg")
player = pygame.image.load("repository/spaceship.png")
enemy = pygame.image.load("repository/enemyship.png")
superenemy = pygame.image.load("repository/enemyship_hard.png")
blinkplayer = pygame.image.load("repository/spaceship_hit.png")
HPImage = pygame.image.load("repository/Transparent.png")
player = pygame.transform.smoothscale(player, (63, 63))
enemy = pygame.transform.smoothscale(enemy, (63, 63))
blinkplayer = pygame.transform.smoothscale(blinkplayer, (63, 63))
superenemy = pygame.transform.smoothscale(superenemy, (63, 63))
background = pygame.image.load("repository/spacebg.jpg")
gfont = pygame.font.Font("simhei.ttf", 25)
btfont = pygame.font.Font("simhei.ttf", 60)
stfont = pygame.font.Font("simhei.ttf", 50)
white = (255, 255, 255)
title1 = btfont.render("Aircraft Battle2", True, white)
title2 = stfont.render("by AbsoCube Studio", True, white)
title1_rect = title1.get_rect()
title1_rect.centerx = 300
title1_rect.centery = 100
title2_rect = title2.get_rect()
title2_rect.centerx = 300
title2_rect.centery = 200
start = button(50, 300, 500, 35, "Play", gfont, (255, 0, 0), white)
back = button(50, 300, 500, 35, "Back", gfont, (0, 255, 0), white)
pygame.mixer.init(frequency=44100)
musicSHOOT = "repository/laser.wav"
musicBG = "repository/starfleet.mp3"
stop = True
oldCondition = False
bullets = []
enemyPlanes = []
shoot = False
makeEnemy = time.time()
gameStart = 0
hard = 1
superEnemy = False
playerHP = 5
HPPos = 600
blink = False
over = False
heldOutTime = 0

# first show logo
oldtime = time.time()
screen.fill((255, 255, 255))
screen.blit(AC, (172, 72))
pygame.display.update()
time.sleep(3)

# main programme begin
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and not stop:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(musicSHOOT)
            pygame.mixer.music.play()
            shoot = True
        elif start.pressed(event) and stop and not over:
            stop = False
            gameStart = time.time()
            playerHP = 5
            bullets = []
            enemyPlanes = []
            HPPos = 600
        elif back.pressed(event) and over:
            over = False
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    x, y = pygame.mouse.get_pos()

    # background
    screen.blit(background, (0, 0))

    # play music
    if oldCondition != stop:
        if stop:
            pygame.mixer.music.load(musicBG)
            pygame.mixer.music.play(True)
        elif not stop:
            pygame.mixer.music.stop()
        oldCondition = stop

    if stop and not over:
        # game's cover
        screen.blit(title1, title1_rect)
        screen.blit(title2, title2_rect)
        start.show(screen)

    elif not stop and not over:
        # game difficulty
        if 3 <= time.time() - gameStart <= 5:
            hard = 0.9
        elif 5 <= time.time() - gameStart <= 8:
            hard = 0.8
        elif 8 <= time.time() - gameStart <= 13:
            hard = 0.7
        elif time.time() - gameStart > 13:
            superEnemy = True

        # show HP
        if HPPos > playerHP * 120:
            HPPos -= 1
        else:
            blink = False
        screen.blit(HPImage, (HPPos, 0))

        # blinking
        if blink is True:
            showplayer = blinkplayer
        else:
            showplayer = player

        # print player
        x -= 300
        y -= 200
        angle = math.atan2(y, x)
        bangle = math.radians(-math.degrees(angle) + 90)
        rangle = -math.degrees(angle) % 360 - 90
        scratch_player = pygame.transform.rotate(showplayer, rangle)
        width, height = scratch_player.get_size()
        playerpos = 300-width//2, 200-height//2
        screen.blit(scratch_player, playerpos)

        # create a bullet
        if shoot is True:
            shoot = False
            scratch_bullet = {'angle': bangle, 'distance': 0}
            bullets.append(scratch_bullet)

        # create a enemy
        if time.time()-makeEnemy >= 0.8:
            direction = random.randint(1, 360)
            scratch_enemy = {'direction': direction, 'distance': 300, 'HP': 1}
            if superEnemy:
                sEnemy = random.randint(1, 2)
                scratch_enemy['HP'] = sEnemy
            enemyPlanes.append(scratch_enemy)
            makeEnemy = time.time()

        # print bullets
        if bullets:
            bOrder = -1
            for bullet in bullets:
                bOrder += 1
                bullet['distance'] += 1
                posx = 300 + math.sin(bullet['angle'])*bullet['distance']
                posy = 200 + math.cos(bullet['angle'])*bullet['distance']
                BStart = (int(posx), int(posy))
                posx = 300 + math.sin(bullet['angle']) * (bullet['distance'] + 10)
                posy = 200 + math.cos(bullet['angle']) * (bullet['distance'] + 10)
                BEnd = (int(posx), int(posy))
                pygame.draw.line(screen, white, BStart, BEnd)
                # touch edge?
                if BStart[0] >= 600 or BStart[0] <= 0 or BStart[1] >= 400 or BStart[1] <= 0:
                    del bullets[bOrder]
        # print enemy
        if enemyPlanes:
            order = -1
            for enemyPlane in enemyPlanes:
                order += 1
                enemyPlane['distance'] -= 0.5
                if enemyPlane['HP'] == 2:
                    printenemy = superenemy
                else:
                    printenemy = enemy
                scratch_enemy_plane = pygame.transform.rotate(printenemy, enemyPlane['direction'])
                width, height = scratch_enemy_plane.get_size()
                eAngle = math.radians(enemyPlane['direction'])
                posx = 300 + math.sin(eAngle)*enemyPlane['distance'] - width // 2
                posy = 200 + math.cos(eAngle)*enemyPlane['distance'] - height // 2
                ePos = (int(posx), int(posy))
                screen.blit(scratch_enemy_plane, ePos)
                enemy_plane_rect = scratch_enemy_plane.get_rect()
                bOrder = -1
                for bullet in bullets:
                    # hit?
                    bOrder += 1
                    if enemyPlane['distance'] <= bullet['distance']:
                        bPosx = 300 + math.sin(bullet['angle']) * bullet['distance']
                        bPosy = 200 + math.cos(bullet['angle']) * bullet['distance']
                        if posx-enemy_plane_rect.width-20 < bPosx < posx+enemy_plane_rect.width-20:
                            if posy-enemy_plane_rect.height-20 < bPosy < posy+enemy_plane_rect.height-20:
                                enemyPlane['HP'] -= 1
                                del bullets[bOrder]
                if enemyPlane['distance'] <= 0:
                    del enemyPlanes[order]
                    playerHP -= 1
                    blink = True
                if enemyPlane['HP'] <= 0:
                    del enemyPlanes[order]
        # death?
        if playerHP <= 0:
            over = True
            heldOutTime = time.time() - gameStart

    # screen when game is over
    else:
        stop = True
        title = btfont.render("Game Over", True, white)
        text = stfont.render("You held out for {:.1f}S".format(heldOutTime), True, white)
        title_rect = title.get_rect()
        title_rect.centerx = 300
        title_rect.centery = 100
        text_rect = text.get_rect()
        text_rect.centerx = 300
        text_rect.centery = 200
        screen.blit(title, title_rect)
        screen.blit(text, text_rect)
        back.show(screen)
    pygame.display.update()
