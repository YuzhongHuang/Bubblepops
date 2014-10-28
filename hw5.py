# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 13:01:36 2014

@author: yuzhong
"""

"""
Anders Johnson
Yuzhong Huang

Software Design
10/8/14

HW5: Video Game

"""

import pygame
from pygame.locals import *
from sys import exit
import random
import math
import time


class BubbleModel:
    """Create a model for our bubble pop game"""
    def __init__(self):
        color_list = [pygame.Color(200, 0, 250), pygame.Color(250, 150, 150),
                      pygame.Color(80, 80, 200), pygame.Color(10, 255, 200)]
        self.shooter = Shooter([320, 480], [320, 450], 5)
        self.bubbleshooter = BubbleShooter(random.choice(color_list),
                                           [320, 434])
        self.bubbles = []
        # Positions for bubbles in with 20 bubbles in row
        for x_even in range(16, 640, 32):
            for y_even in range(16, 128, 56):
                bubble_color = random.choice(color_list)
                bubble = Bubble(bubble_color, (x_even, y_even))
                self.bubbles.append(bubble)
        # Positions for bubbles with 19 bubbles in row
        for x_odd in range(32, 624, 32):
            for y_odd in range(44, 144, 56):
                bubble_color = random.choice(color_list)
                bubble = Bubble(bubble_color, (x_odd, y_odd))
                self.bubbles.append(bubble)

    def update(self):
        """Detects changes to the model and updates the view"""
        self.collision()
        x_in_range = self.bubbleshooter.pos[0] >= 16 \
        and self.bubbleshooter.pos[0] <= 624
        y_in_range = self.bubbleshooter.pos[1] >= 16 \
        and self.bubbleshooter.pos[1] <= 464
        # allows the ball to bounce off the wall
        if self.bubbleshooter.moving:
            xn = 0
            yn = 0
            a1 = self.bubbleshooter.pos[0] - 320
            b1 = 480 - self.bubbleshooter.pos[1]
            xn += a1 / math.sqrt(a1 ** 2 + b1 ** 2) * 5
            yn += b1 / math.sqrt(a1 ** 2 + b1 ** 2) * 5
            flag = True
            p = 0
            q = 0
            if flag:
                if xn <= 0:
                    self.bubbleshooter.pos[0] += int(xn - 0.5)
                    self.bubbleshooter.pos[1] -= int(yn + 0.5)
                if xn > 0:
                    self.bubbleshooter.pos[0] += int(xn + 0.5)
                    self.bubbleshooter.pos[1] -= int(yn + 0.5)
            if not x_in_range:
                p += 1
                flag = False
            if not y_in_range:
                q += 1
                flag = False
            if p % 2 == 1 and q % 2 == 1:
                self.bubbleshooter.pos[0] -= int(xn + 0.5)
                self.bubbleshooter.pos[1] += int(yn + 0.5)
            if p % 2 == 1 and not q % 2 == 1:
                self.bubbleshooter.pos[0] -= 3 * int(xn + 0.5)
                self.bubbleshooter.pos[1] -= int(yn + 0.5)
            if not p % 2 == 1 and q % 2 == 1:
                self.bubbleshooter.pos[0] += int(xn + 0.5)
                self.bubbleshooter.pos[1] += int(yn + 0.5)

    def collision(self):
        """ This method detects collisions between the bubbles by determining
        if the distance between the centers of the bubbles is <= the diameter
        of a bubble """
        for bubble in self.bubbles:
            if math.sqrt((self.bubbleshooter.pos[0] - bubble.pos[0]) ** 2 + \
            (self.bubbleshooter.pos[1] - bubble.pos[1]) ** 2) <= 34 \
            and math.sqrt((self.bubbleshooter.pos[0] - bubble.pos[0]) ** 2 + \
            (self.bubbleshooter.pos[1] - bubble.pos[1]) ** 2) > 28:
                if bubble.pos[0] >= self.bubbleshooter.pos[0]:
                    self.bubbleshooter.moving = False
                    self.bubbleshooter.stop = False
                    new_bubble = Bubble(self.bubbleshooter.color,
                                       (bubble.pos[0] - 16, bubble.pos[1] +
                                        28))
                    self.bubbles.append(new_bubble)
                if bubble.pos[0] < self.bubbleshooter.pos[0]:
                    self.bubbleshooter.moving = False
                    self.bubbleshooter.stop = False
                    new_bubble = Bubble(self.bubbleshooter.color,
                                       (bubble.pos[0] + 16, bubble.pos[1] +
                                        28))
                    self.bubbles.append(new_bubble)

                if bubble.color == self.bubbleshooter.color:
                    if len(self.neighbor(bubble)) >= 1:
                        self.bubbles.remove(bubble)
                        a = self.neighbor(bubble)
                        for pop_bubble in a:
                            b = self.neighbor(pop_bubble)
                            for pop_bubble in b:
                                if pop_bubble in self.bubbles:
                                    self.bubbles.remove(pop_bubble)
                        for pop_bubble in a:
                            if pop_bubble in self.bubbles:
                                self.bubbles.remove(pop_bubble)

    def is_surrounding(self, contact_bubble, other):
        """Determines which bubbles are surrounding the bubble that
        was contacted"""
        surrounding_list = [(contact_bubble.pos[0] + 32,
                            contact_bubble.pos[1]), (contact_bubble.pos[0] -
                            32, contact_bubble.pos[1]),
                            (contact_bubble.pos[0] + 16, contact_bubble.pos[1]
                            + 28), (contact_bubble.pos[0] - 16,
                            contact_bubble.pos[1] + 28), (contact_bubble.pos[0]
                            + 16, contact_bubble.pos[1] - 28),
                            (contact_bubble.pos[0] - 16, contact_bubble.pos[1]
                            - 28)]
        for i in surrounding_list:
            if other.pos == i:
                return True
        return False

    def neighbor(self, contact_bubble):
        """Wrapper method for add_neighbor"""
        neighbor_list = []
        neighbor_list = self.add_neighbor(neighbor_list, contact_bubble)
        return neighbor_list

    def add_neighbor(self, neighbor_list, contact_bubble):
        """Creates a list for the affected bubbles"""
        for o in self.bubbles:  # "o" is for bubbles!
            if self.is_surrounding(contact_bubble, o) and \
            o.color == contact_bubble.color and o not in neighbor_list:
                if o not in contact_bubble.neighbor_list:
                    contact_bubble.neighbor_list.append(o)
        return contact_bubble.neighbor_list


class Bubble():
    """Build a class for bubble layout"""
    def __init__(self, color, pos, radius=16):
        self.color = color
        self.pos = pos
        self.radius = radius
        self.neighbor_list = []


class Shooter():
    """Build a class for creating the shooter"""
    def __init__(self, start, end, width):
        self.color = (255, 255, 0)
        self.width = width
        self.start = start
        self.end = end


class BubbleShooter():
    """Build a class for shooting the bubbles"""
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.moving = False
        self.stop = True
        self.wall = False


class BubbleWindowView:
    """Bubblepops window view (contains the gui and game screen)"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    # Create the start menu
    def start_screen(self):
        black = (0, 0, 0)
        header = pygame.font.SysFont("timesnewroman", 50)
        starter = pygame.font.SysFont("timesnewroman", 50)
        title = header.render("Bubble Pop!", True, black)
        play = header.render("Play", True, black)
        pic = pygame.image.load("background_scaled.png").convert()
        self.screen.blit(pic, (0, 0))
        self.screen.blit(title, (200, 70))
        self.screen.blit(play, (280, 360))
        pygame.display.update()

    # Draw the features of the game
    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        pygame.draw.line(self.screen, self.model.shooter.color,
                         self.model.shooter.start, self.model.shooter.end, 5)
        pygame.draw.circle(self.screen, self.model.bubbleshooter.color,
                           self.model.bubbleshooter.pos, 16)
        for current_bubble in self.model.bubbles:
            pygame.draw.circle(self.screen, current_bubble.color,
                               current_bubble.pos, 16)
        pygame.display.update()


class BubbleController:
    def __init__(self, model):
        self.model = model

    # Uses MOUSEMOTION to track the mouse location and have the bubble
    # shooter rotate as a result
    def handle_event(self, event):
        #first_click = True
        self.model.collision()
        click = pygame.mouse.get_pressed() == (1, 0, 0)
        if event.type == MOUSEMOTION:
            a = math.atan2((event.pos[0] - 320), (480 - event.pos[1]))
            self.model.shooter.end[0] = 30 * math.sin(a) + 320
            self.model.shooter.end[1] = 480 - 30 * math.cos(a)
            if not self.model.bubbleshooter.moving:
                a = math.atan2((event.pos[0] - 320), (480 - event.pos[1]))
                self.model.bubbleshooter.pos[0] = int(46 * math.sin(a) + 320)
                self.model.bubbleshooter.pos[1] = int(480 - 46 * math.cos(a))
                if not self.model.bubbleshooter.stop:
                    self.model.bubbleshooter.color = \
                    random.choice([pygame.Color(200, 0, 250), \
                    pygame.Color(250, 150, 150),
                    pygame.Color(80, 80, 200), pygame.Color(10, 255, 200)])
                    self.model.bubbleshooter.stop = True
        if click:
            self.model.bubbleshooter.moving = True


def main():
    """This section runs the code for our game"""
    # Initialize pygame
    pygame.init()
    pic_size = (640, 480)
    screen = pygame.display.set_mode((pic_size))
    pygame.display.set_caption("Bubble Pop!")
    white = (255, 255, 255)
    screen.fill(white)

    # Initialize MVC
    model = BubbleModel()
    view = BubbleWindowView(model, screen)
    controller = BubbleController(model)

    view.start_screen()

    starting = running = True

    # Track the position of the mouse and recognize that "PLAY" is clicked
    while starting:
        for event in pygame.event.get():
            if event.type == QUIT:
                starting = running = False
        (x, y) = pygame.mouse.get_pos()
        over_play_button = (x in range(270, 380)) and (y in range(350, 420))
        click = pygame.mouse.get_pressed() == (1, 0, 0)
        if over_play_button and click:
            starting = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()

if __name__ == "__main__":
    main()
