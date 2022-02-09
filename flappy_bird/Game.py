import os
import sys
import pygame
import random
pygame.font.init()
##
# ---------------------------------------------------------------------------
# ---------------------VARIABLES-----------------------------------------
WIDTH, HEIGHT = 336, 550
# window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)


FONT1 = pygame.font.SysFont('comicsans',50)
FONT2 = pygame.font.SysFont('comicsans',30)


FPS = 60
GRAVITY = 5
JUMP_SPEED = 8

START_IMAGE = pygame.image.load(os.path.join('Assets', 'start.png')).convert()
START = pygame.transform.scale(START_IMAGE,(WIDTH,HEIGHT))

BIRD_IMAGE = pygame.image.load(os.path.join('Assets', 'yellowbird-downflap.png')).convert()

BASE_IMAGE = pygame.image.load(os.path.join('Assets', 'base.png'))
base_x_pos = 0
BASE_VELOCITY = 1.5

BG_IMAGE = pygame.image.load(os.path.join('Assets', 'background-night.png'))
BACKGROUND = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

PIPE_IMAGE_1 = pygame.image.load(os.path.join('Assets','pipe-green.png'))
PIPE_1 = pygame.transform.scale(PIPE_IMAGE_1, (55,400))

PIPE_IMAGE_2 = pygame.image.load(os.path.join('Assets','pipe-green.png'))
PIPE_2 = pygame.transform.scale(pygame.transform.rotate(PIPE_IMAGE_2, 180),(55,400))

pipe_x_pos = 400
pipe_y_pos = [400,300,250,200,150]

pipe_height_1 = random.choice(pipe_y_pos)
pipe_height_2 = random.choice(pipe_y_pos)

PIPE_VELOCITY = 5

SCORE = 0

clock = pygame.time.Clock()
# -----------------------#------------------------------#--------------------------#------------------
def main():
    global run
    bird = pygame.Rect(40, 200, 0, 0)

    run = True
    start()
    while run:
        event()

        keys_pressed = pygame.key.get_pressed()
        movement(keys_pressed, bird)

        draw_window(bird)


def draw_window(bird):

    WIN.blit(BACKGROUND, (0, 0))
    moving_pipes()
    moving_floor()
    WIN.blit(BIRD_IMAGE, (bird.x, bird.y))
    DISPLAY_SCORE = FONT1.render("SCORE: " + str(SCORE), 1, WHITE)
    WIN.blit(DISPLAY_SCORE, (80, 10))
    pygame.display.update()


def movement(keys_pressed, bird):

    global SCORE

# -------------------------- CONTROLS---------------------------

    if keys_pressed[pygame.K_SPACE] and bird.y - JUMP_SPEED > 0:
        bird.y -= JUMP_SPEED
    elif bird.y + GRAVITY < 470:
        bird.y += GRAVITY
# ---------------------------------------------------------------


# ------------------------------CHECK FOR COLLISION---------------------------------
    if bird.y - JUMP_SPEED < 0 or bird.y + GRAVITY > 469:
        print("GAME OVER")
        collision(bird)

    if bird.y >= pipe_height_1 - 19 and pipe_x_pos + 55 >= bird.x >= pipe_x_pos - 20:           # PIPE 1
        print("Collision")
        collision(bird)
    if bird.y <= pipe_height_1 - 108 and pipe_x_pos + 55 >= bird.x >= pipe_x_pos - 20:          # PIPE 2
        print("Collision")
        collision(bird)

    if bird.y >= pipe_height_2 - 19 and pipe_x_pos + 430 >= bird.x >= pipe_x_pos + 370:         # NEW PIPE 1
        print("Collision")
        collision(bird)

    if bird.y <= pipe_height_2 - 108 and pipe_x_pos + 430 >= bird.x >= pipe_x_pos + 370:        # NEW PIPE 2
        print("Collision")
        collision(bird)
# --------------------------------------------------------------------------------------------

# ------------------------ ADD ACORE----------------------------------------------------------
    if pipe_x_pos == bird.x or pipe_x_pos + 390 == bird.x:
        SCORE +=1
        print(SCORE)

def moving_floor():
    global base_x_pos

    WIN.blit(BASE_IMAGE, (base_x_pos, 470))
    WIN.blit(BASE_IMAGE, (base_x_pos + 336, 470))
    base_x_pos -= BASE_VELOCITY
    if base_x_pos == -336:
        base_x_pos = 0



def moving_pipes():
    global pipe_x_pos
    global pipe_height_1
    global pipe_height_2


    WIN.blit(PIPE_1, (pipe_x_pos, pipe_height_1))
    WIN.blit(PIPE_2, (pipe_x_pos, (pipe_height_1 - 500)))

    WIN.blit(PIPE_1, (pipe_x_pos + 390, pipe_height_2))
    WIN.blit(PIPE_2, (pipe_x_pos + 390, pipe_height_2 - 500))

    pipe_x_pos -= PIPE_VELOCITY

    if pipe_x_pos <= -430:
        pipe_x_pos = 335
        pipe_height_1 = random.choice(pipe_y_pos)
        pipe_height_2 = random.choice(pipe_y_pos)


def event():
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def collision(bird):
    global BASE_VELOCITY
    global PIPE_VELOCITY
    global pipe_x_pos
    global SCORE


    restart = False
    BASE_VELOCITY = 0               # EVENTUALLY PAUSE GAME
    PIPE_VELOCITY = 0               # ^^^^^^^^^^^^^^^^^^^^^

    while not restart:

        keys_pressed = pygame.key.get_pressed()
        event()
        Restart = FONT1.render("Press R to Restart", 1, WHITE)
        WIN.blit(Restart, (20, 250))
        pygame.display.update()

        if keys_pressed[pygame.K_r]:
            restart = True
            SCORE = 0
            BASE_VELOCITY = 1.5
            PIPE_VELOCITY = 5
            pipe_x_pos = 400
            bird.y = 200
            WIN.blit(BIRD_IMAGE, (40, bird.y))

def start():
    while True:
        event()
        keys_pressed = pygame.key.get_pressed()
        Welcome = FONT1.render("WELCOME", True, WHITE)
        WIN.blit(START, (0, 0))
        WIN.blit(Welcome, (80, 100))
        toStart = FONT2.render("Press SpaceBar to start the game", True, WHITE)
        WIN.blit(toStart, (3, 400))
        pygame.display.update()
        if keys_pressed[pygame.K_SPACE]:
            break



if __name__ == '__main__':
    main()