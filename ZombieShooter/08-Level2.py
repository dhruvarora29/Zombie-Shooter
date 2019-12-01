import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()              #sound

white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255
yellow = 255,255,0

size = width, height = 1200, 500

screen = pygame.display.set_mode(size)      #initialize screen

pointer = pygame.image.load("images/aim_2.png")
gunImage = pygame.image.load("images/gun_1.png")

zombie_1 = pygame.image.load("images/zombie_1.gif")
zombie_2 = pygame.image.load("images/zombie_2.png")
zombie_3 = pygame.image.load("images/zombie_3.png")
zombie_4 = pygame.image.load("images/zombie_4.png")

zombieList = [zombie_1, zombie_2, zombie_3, zombie_4]

bullet_image = pygame.image.load("images/bullet_1.png")

backgroundImage = pygame.image.load("images/background.png")
bloodImage = pygame.image.load("images/zombie_blood.png")

gun_shot = pygame.mixer.Sound("sounds/shot_sound.wav")
background_sound = pygame.mixer.Sound("sounds/background.wav")
background_sound.play(-1)

zombie_shot = pygame.mixer.Sound("sounds/zombie_shot.wav")
zombie_entry = pygame.mixer.Sound("sounds/zombie_entry_1.wav")
reload_gun = pygame.mixer.Sound("sounds/reload.ogg")

clock = pygame.time.Clock()                                  #create object to help track time
FPS = 50

def homeScreen():
    bg_img = pygame.image.load("images/bg.jpg")
    font_1 = pygame.font.Font('fonts/font_1.ttf',70)
    text_1 = font_1.render('Zombie Attack',True,white)
    font_2 = pygame.font.Font('fonts/font_1.ttf',40)
    text_2 = font_2.render('Press Any Key to Start Game',True,red)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                main()

        screen.blit(bg_img, (0,0))
        screen.blit(text_1,(250,100))
        screen.blit(text_2,(200,250))

        pygame.display.update()


def gameOver(counter):
    font = pygame.font.Font(None, 80)
    font_2 = pygame.font.Font('font_1.otf', 50)
    font_3 = pygame.font.Font('font_1.otf', 80)
    seconds_display = font_3.render("Game Over", 1, red)
    seconds_display_2 = font.render("Press any key to start again", 1, yellow)
    scoreDisplay = font_2.render("Total Score is : "+str(counter), True, red)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                main()

        screen.blit(seconds_display, (width/2 - 200, 100))
        screen.blit(seconds_display_2, (width/2-400, 175))
        screen.blit(scoreDisplay, (width / 2 - 200, 250))

        pygame.display.update()

def timer(seconds):
    font = pygame.font.Font(None, 46)
    seconds_display = font.render("Time Left: " + str(seconds), 1, yellow)
    screen.blit(seconds_display, (width-400, 10))

def score(c):
    font = pygame.font.Font('font_1.otf', 50)
    text = font.render("Score : "+str(c), True, yellow)
    screen.blit(text, (10,10))
    file = open('score.txt','w')
    file.write(str(c))

def level():
    font = pygame.font.SysFont(None, 80)
    text = font.render("Level Completed", True, red)
    text_1 = font.render("Press SPACE to restart", True, white )

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.type==pygame.K_SPACE:
                main()
        screen.blit(text, (300,100))
        screen.blit(text_1, (500, 200))
        pygame.display.update()

def bloodPatch(mouse_pos_x, mouse_pos_y):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        screen.blit(bloodImage, (mouse_pos_x - 50, mouse_pos_y - 50))
        pygame.display.update()
        clock.tick(10)
        break

def bulletsCounter(shot):
    font = pygame.font.Font(None, 35)
    text = font.render("Bullets Left : "+str(shot), True, red)
    if shot == 0:
        text = font.render("Press R", True, red)
        text_1 = font.render("to Reload", True, red)
        screen.blit(text_1, (width - 180,140))
    elif shot >= 1:
        text = font.render("Bullets Left : "+str(shot), True, red)
    screen.blit(text, (width - 180,100))

def main():
    zombie_x = random.randint(0,width-400)
    zombie_y = random.randint(0,height-200)
    zombieImage = random.choice(zombieList)

    zombieScaleX = 130
    zombieScaleY = 180

    bullets = []
    for i in range(4):
        bullets.append(bullet_image)

    gun_y = height/2+30

    counter = 0
    clicked = 0
    shot = 4

    seconds = 30
    pygame.time.set_timer(USEREVENT + 1, 1000)

    game = True
    while game:

        screen.fill(white)
        screen.blit(backgroundImage, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT :
                quit()
            elif event.type == USEREVENT + 1:
                seconds -= 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==BUTTON_LEFT:
                if shot == 0:
                    pass
                elif shot >= 1 :
                    gun_shot.play()

                    #mouse_pos_y-=100                                                      #1
                    shot -= 1

                    # bullets.pop()
                    if rect_1.colliderect(rect_2):
                        clicked += 1
                        zombieImage = pygame.transform.scale(zombieImage, (zombieScaleX, zombieScaleY))
                        zombieScaleX -= 10
                        zombieScaleY -= 10
                        if clicked == 3:
                            zombie_shot.play()
                            bloodPatch(mouse_pos_x, mouse_pos_y)
                            zombie_x = random.randint(0,width-400)
                            zombie_y = random.randint(0,height-200)
                            zombieImage = random.choice(zombieList)
                            counter += 1
                            clicked = 0
                            zombieScaleX = 100
                            zombieScaleY = 150
                            zombie_entry.play()

            elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_r:
                    shot = 4
                    reload_gun.play(0)

            elif event.type == pygame.MOUSEBUTTONUP:
                gun_y = height/2+30


        if seconds == -1:
            gameOver(counter)

        if counter == 20:
            level()

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

        screen.blit(zombieImage, (zombie_x, zombie_y))
        screen.blit(pointer, (mouse_pos_x - 50, mouse_pos_y - 50))
        screen.blit(gunImage, (mouse_pos_x,gun_y))

        for i in range(shot):
            screen.blit(bullets[i], (width-40 * (i+1), height/2 - 100))

        rect_1 = pygame.Rect(mouse_pos_x-50, mouse_pos_y-50, pointer.get_width(), pointer.get_height())

        rect_2 = pygame.Rect(zombie_x, zombie_y, zombieImage.get_width(), zombieImage.get_height())

        score(counter)
        timer(seconds)
        bulletsCounter(shot)

        pygame.display.update()
        clock.tick(FPS)

    quit()

#main()
homeScreen()