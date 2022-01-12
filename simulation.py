from body import Body
from body import update_bodies
from frames import *
from game_utilities import *
from slider import Slider
from button import Button
from settings import Settings

import math
import numpy as np

import sys
import pygame
import copy

"""Pygame parameters"""
pygame.init()

width = 720
height = 720
screen_color = (0, 0, 0)

screen = pygame.display.set_mode((width, height))

pressed = False
slider_enabled = False
click_pos = ()
mouse_click_pos = ()
camera_origin = [0, 0]
settings = Settings(width, height, camera_origin, screen_color)


""" Simulation parameters"""
orbita_geo = 36 * 10**6  # m
radio_tierra = 6371000  # m
earth_mass = 5.972 * 10**24


r1 = np.array([0, orbita_geo + radio_tierra])
v1 = np.array([-3075, 0])
body1 = Body(100, r1, v1)


r2 = np.array([0, 0])
v2 = np.array([0, 0])
body2 = Body(earth_mass, r2, v2)


objects = [body1, body2]


# T = 1000
# r1 = np.array([0, 0])
# v = np.array([0, 0])
# body1 = Body(10**5, r1, v)
#
# r2 = np.array([-T/3, -T/3])
# r3 = np.array([-2*T/3, -2*T/3])
# body2 = Body(10**5, r2, v)
# body3 = Body(10**5, r3, v)
#
# objects = [body1, body2, body3]

# objects = []


position_list = []


""" pause button """
start_button = Button((550 - 50/2, 10), 50, 20, (255, 255, 255), (128, 128, 128))

""" Slider """
slider_init_position = (600, 20)
slider = Slider(slider_init_position, 25, 100, 10**10, 10**25, (255, 255, 255), 50)

while True:
    # input
    click_pos = pygame.mouse.get_pos()

    if start_button.rect.collidepoint(click_pos):
        start_button.hover = True
    else:
        start_button.hover = False

    if settings.pause_menu:
        """ Pause mode"""

        for event in pygame.event.get():
            handle_menu_events(event, click_pos, start_button, slider, settings)

        # update game
        simulation_results = update_menu_data(click_pos, objects, start_button, slider, settings)

        # Render
        draw_menu(screen, objects, simulation_results, start_button, slider, settings)

        # To update simulation time with mode change
        if not settings.pause_menu:
            settings.t1 = pygame.time.get_ticks()

    else:
        """ Real time simulation"""

        for event in pygame.event.get():
            handle_simulation_events(event, click_pos, start_button, slider, settings)

        # update game
        simulation_results = update_simulation_data(click_pos, objects, start_button, slider, settings)

        # Render
        draw_simulation(screen, objects, simulation_results, start_button, slider, click_pos, settings)



