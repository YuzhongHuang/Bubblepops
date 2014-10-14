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


def main_screen():
    """
    In this part of the assignment, we created a GUI for our Bubble Pop game.
    """

    black = (0, 0, 0)
    white = (255, 255, 255)
    pic_size = (350, 350)
    pygame.init()
    screen = pygame.display.set_mode((pic_size))

    pygame.display.set_caption("Bubble Pop!")
    screen.fill(white)
    """
    For some reason, comicsansms isn't working, so I used Times New Roman.
    We can change this.
    """
    header = pygame.font.SysFont("timesnewroman", 30)
    starter = pygame.font.SysFont("timesnewroman", 30)
    title = header.render("Bubble Pop!", True, black)
    play = header.render("Play", True, black,)
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
        (x, y) = pygame.mouse.get_pos()
        over_play_button = (x in range(140, 220)) and (y in range(240, 290))
        click = pygame.mouse.get_pressed() == (1, 0, 0)
        if over_play_button and click and first_click:
            screen.fill(black)
            message = starter.render("You've pressed play!", True, white)
            screen.blit(message, (45, 70))
            first_click = False

        pygame.display.flip()

    pygame.quit()
if __name__ == "__main__":
    main_screen()
