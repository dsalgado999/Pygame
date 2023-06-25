import pygame as p
import random as r
import math as m

p.init()

# WINDOW_MEASURE
WIDTH, HEIGHT = 800, 600
# WINDOW
win = p.display.set_mode((WIDTH, HEIGHT))

# WINDOW_CAPTION
p.display.set_caption("First Game")
# WINDOW_ICON
icon = p.image.load('pygame/astronave.png')
p.display.set_icon(icon)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# PLAYERS
playerImg = p.image.load('pygame/spacecraft.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(p.image.load('pygame/enemigo.png'))
    enemyX.append(r.randint(0, 800))
    enemyY.append(r.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
bulletImg = p.image.load('pygame/bala.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

font = p.font.Font('freesansbold.ttf', 32)

score_value = 0
textX = 10
textY = 10

# Game over Text
over_font = p.font.Font('freesansbold.ttf', 56)

game_state = "menu"  # Variable para controlar el estado del juego: "menu", "playing", "game_over"


def show_score(X, Y):
    global score_value
    score_text = font.render("Score :" + str(score_value), True, (255, 255, 255))
    win.blit(score_text, (X, Y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


def player(X, Y):
    win.blit(playerImg, (X, Y))


def enemy(X, Y, i):
    win.blit(enemyImg[i], (X, Y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = m.sqrt((m.pow(enemyX - bulletX, 2)) + (m.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_menu():
    title_font = p.font.Font('freesansbold.ttf', 64)
    title_text = title_font.render("Space Invaders", True, WHITE)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    start_font = p.font.Font('freesansbold.ttf', 32)
    start_text = start_font.render("Press SPACE to Start", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    win.blit(title_text, title_text_rect)
    win.blit(start_text, start_text_rect)


# GAME LOOP
run = True
while run:
    win.fill(BLACK)

    if game_state == "menu":
        show_menu()

    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
        if game_state == "menu":
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                game_state = "playing"
        elif game_state == "playing":
            # if keystroke is pressed check whether its right or left
            if event.type == p.KEYDOWN:
                if event.key == p.K_RIGHT:
                    playerX_change = 0.3
                if event.key == p.K_LEFT:
                    playerX_change = -0.3
                if event.key == p.K_UP:
                    playerY_change = -0.3
                if event.key == p.K_DOWN:
                    playerY_change = 0.3
                if event.key == p.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == p.KEYUP:
                if event.key == p.K_RIGHT or event.key == p.K_LEFT:
                    playerX_change = 0
                if event.key == p.K_UP or event.key == p.K_DOWN:
                    playerY_change = 0

    if game_state == "playing":
        # barreras
        playerX += playerX_change
        playerY += playerY_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        if playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536

        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 200:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_state = "game_over"
                break

            if enemyX[i] <= 0:
                enemyX[i] = 0
            elif enemyX[i] >= 736:
                enemyX[i] = 736

            if enemyY[i] <= 0:
                enemyY[i] = 0
            elif enemyY[i] >= 536:
                enemyY[i] = 536

            # enemy movement
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                print(score_value)
                enemyX[i] = r.randint(0, 800)
                enemyY[i] = r.randint(20, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    elif game_state == "game_over":
        game_over_text()

    p.display.update()

p.quit()
