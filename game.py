import random
import sys
import pygame
from pygame.locals import *

FPS=30
SCRWDT = 820
SCRHT = 625
SCR = pygame.display.set_mode((SCRWDT, SCRHT))
GRN_Y = int(SCRHT * 0.85)
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
HS = 0

def welcomeSCR(pts):
    playerx = int(SCRWDT/5)
    playery = int((SCRHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCRWDT - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCRHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                mainGame()
            else:
                SCR.blit(GAME_SPRITES['background'], (0, 0))    
                SCR.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCR.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCR.blit(GAME_SPRITES['base'], (basex, GRN_Y))
                SCR.blit(GAME_SPRITES['score'], (0, 0))
                a=155
                b=185
                offset=0
                global HS
                if pts>HS:
                    HS=pts
                myDigits = [int(x) for x in list(str(pts))]
                for digit in myDigits:
                    SCR.blit(GAME_SPRITES['numbers'][digit], (a+offset, 0))
                    offset+=25
                SCR.blit(GAME_SPRITES['hs'], (0, 40))
                offset=0
                myDigit = [int(x) for x in list(str(HS))]
                for digit in myDigit:
                    SCR.blit(GAME_SPRITES['numbers'][digit], (b+offset, 40))
                    offset+=25
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
            


def mainGame():
    FPS = 30
    score = 0
    playerx = int(SCRWDT/5)
    playery = int(SCRWDT/2)
    basex = 0

  
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

   
    upperPipes = [
        {'x': SCRWDT+200, 'y':newPipe1[0]['y']},
        {'x': (SCRWDT+200+(SCRWDT/2)), 'y':newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCRWDT+200, 'y':newPipe1[1]['y']},
        {'x': (SCRWDT+200+(SCRWDT/2)), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) 
        if crashTest:
            welcomeSCR(score)
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                FPS = FPS+5
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GRN_Y - playery - playerHeight)

       
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCR.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCR.blit(GAME_SPRITES['pipe'][0], (int(upperPipe['x']), int(upperPipe['y'])))
            SCR.blit(GAME_SPRITES['pipe'][1], (int(lowerPipe['x']), int(lowerPipe['y'])))

        SCR.blit(GAME_SPRITES['base'], (basex, GRN_Y))
        SCR.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCRWDT - width)/2

        for digit in myDigits:
            SCR.blit(GAME_SPRITES['numbers'][digit], (int(Xoffset), int(SCRHT*0.12)))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
    
    
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GRN_Y - 53  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCRHT/5
    y2 = offset*1.6 + random.randrange(0, int(SCRHT - GAME_SPRITES['base'].get_height()  - 1.8 *offset))
    pipeX = SCRWDT + 2
    y1 = pipeHeight - y2 + offset*1.2
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe



pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
GAME_SPRITES['score'] =pygame.image.load('gallery/sprites/score.png')
GAME_SPRITES['hs'] =pygame.image.load('gallery/sprites/hs.png')
GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    
GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeSCR(0)
    

