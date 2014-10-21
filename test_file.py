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
    """ Create a model for our bubble pop game"""
    def __init__(self):
        color_list=[(200,0,250),(250,150,150),(80,80,200),(10,255,200)]
        self.shooter=Shooter([320,480],[320,450],5)
        self.bubbleshooter=BubbleShooter(random.choice(color_list),[320,434])
        self.bubbles = []
        # Positions for bubbles in with even number in rows
        for x_even in range(16,640,32):
            for y_even in range(16,128,56):
            	color_list = [(200,0,250),(250,150,150),(80,80,200),(10,255,200)]
            	bubble_color = random.choice(color_list)
            	bubble = Bubble(bubble_color,(x_even,y_even))
            	self.bubbles.append(bubble)
    	
    	for x_odd in range(32,624,32):
            for y_odd in range(44,144,56):
            	color_list = [(200,0,250),(250,150,150),(80,80,200),(10,255,200)]
            	bubble_color = random.choice(color_list)
            	bubble = Bubble(bubble_color,(x_odd,y_odd))
            	self.bubbles.append(bubble)
        

class Bubble():
    """ Build a class for bubble layout"""
    def __init__(self, color, position, radius=16):
        self.color = color
        self.position = position
        self.radius = radius

class Shooter():
    """bulid a class of Shooter"""
    def __init__(self,start,end,width):
        self.color=(255,255,0)
        self.width=width
        self.start=start
        self.end=end

class BubbleShooter():
    """build a class of bubble shooter"""
    def __init__(self,color,pos):

        self.color=color
        self.pos=pos


            
class BubbleWindowView:
    """Bubblepops window view"""
    def __init__(self,model,screen):
        self.model=model
        self.screen=screen
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.line(self.screen, 
                         pygame.Color(self.model.shooter.color[0],
                         self.model.shooter.color[1],
                         self.model.shooter.color[2]),
                         self.model.shooter.start,
                         self.model.shooter.end, 5)
        pygame.draw.circle(self.screen, 
        	               pygame.Color(self.model.bubbleshooter.color[0],
        	               self.model.bubbleshooter.color[1],
        	               self.model.bubbleshooter.color[2]),
                           self.model.bubbleshooter.pos, 16, 0)        
        for current_bubble in self.model.bubbles:
            pygame.draw.circle(self.screen, 
                               pygame.Color(current_bubble.color[0],
                                            current_bubble.color[1],
                                            current_bubble.color[2]), 
                                            current_bubble.position, 16)
        pygame.display.update()


class BubbleController:
    def __init__(self,model):
        self.model = model
    
    def handle_mouse_event(self,event):
        first_click=True
        click=pygame.mouse.get_pressed() != (1, 0, 0)
        if event.type == MOUSEMOTION:
            a=math.atan2((event.pos[0]-320),(480-event.pos[1]))
            self.model.shooter.end[0] = 30*math.sin(a)+320
            self.model.shooter.end[1] = 480-30*math.cos(a)
        if event.type == MOUSEMOTION and click:
            a=math.atan2((event.pos[0]-320),(480-event.pos[1]))
            self.model.bubbleshooter.pos[0]=int(46*math.sin(a)+320)
            self.model.bubbleshooter.pos[1]=int(480-46*math.cos(a))
        if not click:
            first_click=False
        xn=0
        yn=0
        if not first_click:
            for i in range(2):
                a1=self.model.bubbleshooter.pos[0]-320
                b1=480-self.model.bubbleshooter.pos[1]
                xn+=a1/math.sqrt(a1**2+b1**2)*10
                yn+=b1/math.sqrt(a1**2+b1**2)*10
                self.model.bubbleshooter.pos[0] =self.model.bubbleshooter.pos[0]+int(xn)
                self.model.bubbleshooter.pos[1] =self.model.bubbleshooter.pos[1]-int(yn)
            
                

if __name__ == "__main__":
    """
    In this part of the assignment, we created a GUI for our Bubble Pop game.
    """
    black = (0, 0, 0)
    white = (255, 255, 255)
    pic_size = (640, 480)
    pygame.init()
    screen = pygame.display.set_mode((pic_size))
    pygame.display.set_caption("Bubble Pop!")
    screen.fill(white)
    """
    For some reason, comicsansms isn't working, so I used Times New Roman.
    We can change this.
    """
    header = pygame.font.SysFont("timesnewroman", 50)
    starter = pygame.font.SysFont("timesnewroman", 50)
    title = header.render("Bubble Pop!", True, black)
    play = header.render("Play", True, black,)
    pic = pygame.image.load("background_scaled.png").convert()
    screen.blit(pic, (0, 0))
    screen.blit(title, (200, 70))
    screen.blit(play, (280, 360))
    pygame.display.update()
    first_click = True
    while True:
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (x, y) = pygame.mouse.get_pos()
        over_play_button = (x in range(270, 380)) and (y in range(350, 420))
        click = pygame.mouse.get_pressed() == (1, 0, 0)
        if over_play_button and click and first_click:
            size = (640,480)
            screen = pygame.display.set_mode(size)
            
            model = BubbleModel()
            view = BubbleWindowView(model,screen)
            controller = BubbleController(model)
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == MOUSEMOTION:
                        controller.handle_mouse_event(event)
                view.draw()
                time.sleep(.001)
            first_click = False

	pygame.display.flip()

    pygame.quit()
    

    # main_screen()
