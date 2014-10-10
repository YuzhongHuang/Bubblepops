"""
Anders Johnson
Toni Saylor
Yuzhong Huang

Software Design
10/8/14

HW5: Video Game

"""

import pygame
from pygame.locals import *
from sys import exit

black = (0, 0, 0)
white = (255, 255, 255)
pic_size = (350, 350)


def main_screen():
    """
    In this part of the assignment, we created a GUI for our Bubble Pop game.
    """
    pygame.init()
    screen = pygame.display.set_mode((pic_size))  # , 0, 24)
    #screen.fill(pygame.Color(255, 255, 255))
    # pygame.draw.rect(screen,pygame.Color(0,0,0),pygame.Rect(30,30,30,30))
    # pygame.display.update()
    pygame.display.set_caption("Bubble Pop!")
    screen.fill(white)
    """
    For some reason, comicsansms isn't working, so I used Times New Roman.
    We can change this.
    """
    header = pygame.font.SysFont("timesnewroman", 30)
    starter = pygame.font.SysFont("timesnewroman", 30)
    title = header.render("Bubble Pop!", True, black)  # , (white))
    play = header.render("Play", True, black,)  # , (white))
    pic = pygame.image.load("background.png").convert()
    screen.blit(pic, (0, 0))
    screen.blit(title, (100, 70))
    screen.blit(play, (150, 250))
    pygame.display.update()
    first_click = True
    while True:
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (x,y)=pygame.mouse.get_pos()
        over_play_button = (x in range(140, 220)) and (y in range(240, 290))
        click = pygame.mouse.get_pressed() == (1, 0, 0)
        if over_play_button and click and first_click:
            screen.fill(black)
            message = starter.render("You've pressed play!", True, white)
            screen.blit(message, (45, 70))
            first_click = False

        pygame.display.flip()
        
        """
        The clicking feature isn't working, but it recoginzes when the
        mouse is in range.  Yay!  We will work on the clicking feature
        next and we should be done!  Double yay!
        """
            # if pygame.mouse.get_pressed()[1]:
                # print "You pressed play!"

    # if i in range pygame.mouse.get_pos((130,210),(230,290)) and pygame.mouse.pressed():
    #      print "You pressed play!"
    pygame.quit()
if __name__ == "__main__":
    main_screen()
