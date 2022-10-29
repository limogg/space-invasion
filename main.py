import pygame
import random
import math
from pygame import mixer

# Inicjacja
pygame.init()

# Okno
screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load("space.png")

# tytuł
pygame.display.set_caption("Space Invaders by Piotr Janicki")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# tło
playerImg = pygame.image.load("battleship.png")

# dzwięk
mixer.music.load("background.wav")
mixer.music.play(-1)

# gracz
playerX = 600
playerY = 640
playerX_change = 0

# kosmita
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 12

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 1200))
    alienY.append(random.randint(30, 150))
    alienX_change.append(-5)
    alienY_change.append(80)

# laser
laserImg = pygame.image.load("laser.png")
laserX = 0
laserY = 600
laserY_change = 10
laser_state = "ready"

# wynik
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 20
textY = 20

game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    game_over_text = game_over_font.render("Koniec gry twój wynik to: " + str(score_value), True, (255, 255, 255))
    screen.blit(game_over_text, (200, 300))


def show_score(x, y):
    score = font.render("Wynik: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_laser_right(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x - 12, y + 10))


def fire_laser_left(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 43, y + 10))


def isCollision(alienX, alienY, laserX, laserY):
    distance = math.sqrt((math.pow(alienX - laserX, 2)) + (math.pow(alienY - laserY, 2)))
    if distance < 50:
        return True
    else:
        return False


# Pętla gry
running = True

while running:
    # kolor tła
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pętla gracza
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                playerX_change = -8
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                playerX_change = 8
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserX = playerX
                    fire_laser_left(laserX, laserY)
                    laser_sound = mixer.Sound("laser.wav")
                    laser_sound.play()
                    fire_laser_right(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord("a") or event.key == ord(
                    "d"):
                playerX_change = 0

    # granice
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1216:
        playerX = 1216

    # Pętla kosmitów
    for i in range(num_of_aliens):

        if alienY[i] > 600:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] *= -1
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 1216:
            alienX_change[i] *= -1
            alienY[i] += alienY_change[i]
        # kolizja
        collision = isCollision(alienX[i], alienY[i], laserX, laserY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            laserY = 600
            laser_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 1216)
            alienY[i] = random.randint(30, 150)

        alien(alienX[i], alienY[i], i)
    # ruch lasera
    if laserY <= 0:
        laserY = 600
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser_left(laserX, laserY)
        fire_laser_right(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
