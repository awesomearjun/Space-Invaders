import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

bg = pygame.image.load('background.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders ")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
scoreValue = 0

overGame = pygame.font.Font("freesansbold.ttf", 64)


def gameOverText():
    overtext = overGame.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))


def showScore(x, y):
    global scoreValue
    score = font.render(f"Score: {str(scoreValue)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerXChange = 0
playerYChange = 0

enimyImg = []
enimyX = []
enimyY = []
enimyXChange = []
enimyYChange = []
enimys = 100
for i in range(enimys):
    enimyImg.append(pygame.image.load('spaceInvader.png'))
    enimyX.append(random.randint(0, 800))
    enimyY.append(random.randint(50, 150))
    enimyXChange.append(4.6)
    enimyYChange.append(4.6)

bulletImg = pygame.image.load('bullet.png')
bulletY = 480
bulletX = 0
bulletYChange = 10
bulletState = "ready"


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enimy(x, y):
    screen.blit(enimyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    d = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if d < 27:
        return True
    else:
        return False


running = True
while running:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -4.6
            if event.key == pygame.K_RIGHT:
                playerXChange = 4.6
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound('laser.wav')
                bulletSound.play()
                if bulletState is "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    playerX += playerXChange

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # ------------------- #
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    for i in range(enimys):

        if enimyY[i] > 320:
            for j in range(enimys):
                enimyY[j] = 2000
            gameOverText()
            break

        enimyX[i] += enimyXChange[i]
        if enimyX[i] <= 0:
            enimyXChange[i] = 3.6
            enimyY[i] += enimyYChange[i]
        elif enimyX[i] >= 736:
            enimyXChange[i] = -3.6
            enimyY[i] += enimyYChange[i]

        collision = isCollision(enimyX[i], enimyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            enimyX[i] = random.randint(0, 735)
            enimyY[i] = random.randint(50, 150)
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()

        enimy(enimyX[i], enimyY[i])

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
