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


""" Menu """
start_menu = True

start_button = Button((550 - 50/2, 10), 50, 20, (255, 255, 255), (128, 128, 128))

""" Slider """
slider_init_position = (600, 20)
slider = Slider(slider_init_position, 25, 100, 10**10, 10**25, (255, 255, 255), 50)

while start_menu:
    click_pos = pygame.mouse.get_pos()

    if start_button.rect.collidepoint(click_pos):
        start_button.hover = True
    else:
        start_button.hover = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_click_pos = click_pos

            if start_button.hover:
                start_menu = False
            elif slider.rect.collidepoint(mouse_click_pos[0], mouse_click_pos[1]):
                slider_enabled = True
            else:
                pressed = True

                line_init = mouse_click_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if pressed:
                # Add new body
                new_object = new_body_on_click_position(mouse_click_pos, click_pos, slider.value, settings)
                objects.append(new_object)

                pressed = False

            slider_enabled = False

    # update game
    if slider_enabled:
        slider.update_cursor_position(click_pos)

    # Render
    screen.fill(settings.screen_color)

    start_button.draw(screen)
    slider.draw(screen)

    if pressed:
        #pygame.draw.line(screen, (255, 255, 255), line_init, click_pos)

        # Simulate trajectory of object
        delta_t = 120  # 1 min
        n_steps = 1000

        simulate_object = new_body_on_click_position(mouse_click_pos, click_pos, slider.value, settings)
        objects_test = copy.deepcopy(objects)
        objects_test.append(simulate_object)

        position_list = update_bodies(objects_test, delta_t, n_steps)

    for idx, obj in enumerate(objects):

        camera_coord = world_to_camera_coordinates(obj.r, settings.camera_origin)
        screen_coord = world_to_screen_coordinates(camera_coord, width, height)

        radius = max(3, round(math.log(objects[idx].m, 10) / math.log(earth_mass, 10) * 10))

        if width > screen_coord[0] > 0 and height > screen_coord[1] > 0:
            pygame.draw.circle(screen, (255, 255, 255), screen_coord, radius)

    for idx, obj in enumerate(position_list):
        pos = position_list[idx][0, :]

        camera_coord = world_to_camera_coordinates(pos, settings.camera_origin)
        screen_coord = world_to_screen_coordinates(camera_coord, settings.width, settings.height)

        # radius = max(3, round(math.log(slider.value, 10) / math.log(earth_mass, 10) * 10))
        #
        # if settings.width > screen_coord[0] > 0 and settings.height > screen_coord[1] > 0:
        #     pygame.draw.circle(screen, (255, 255, 255), screen_coord, radius)

        for step in range(position_list[idx].shape[0] - 1):
            pos_t1 = position_list[idx][step]
            camera_coord_t1 = world_to_camera_coordinates(pos_t1, settings.camera_origin)
            screen_coord_t1 = world_to_screen_coordinates(camera_coord_t1, settings.width, settings.height)

            pos_t2 = position_list[idx][step + 1]
            camera_coord_t2 = world_to_camera_coordinates(pos_t2, settings.camera_origin)
            screen_coord_t2 = world_to_screen_coordinates(camera_coord_t2, settings.width, settings.height)

            pygame.draw.line(screen, (255, 255, 255), screen_coord_t1, screen_coord_t2)

    pygame.display.flip()


t1 = pygame.time.get_ticks()

""" Main Loop """
while True:

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_pos = pygame.mouse.get_pos()

            if slider.rect.collidepoint(mouse_click_pos[0], mouse_click_pos[1]):
                slider_enabled = True
            else:
                # draw line
                if not pressed:
                    pressed = True

                    line_init = mouse_click_pos

        if event.type == pygame.MOUSEBUTTONUP:

            if pressed:

                # Add new body
                click_pos = pygame.mouse.get_pos()

                new_body = new_body_on_click_position(mouse_click_pos, click_pos, slider.value, settings)
                objects.append(new_body)

                pressed = False

            slider_enabled = False

    # update game
    t2 = pygame.time.get_ticks()
    delta_t = (t2 - t1)
    t1 = t2  # TODO: aqui o tras actualizar los cuerpos?

    position_list = update_bodies(objects, delta_t, 1)

    if slider_enabled:
        click_pos = pygame.mouse.get_pos()
        slider.update_cursor_position(click_pos)

    # render
    screen.fill(settings.screen_color)

    slider.draw(screen)

    if pressed:
        click_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), line_init, click_pos)

    for idx, obj in enumerate(position_list):

        pos = position_list[idx][-1, :]

        camera_coord = world_to_camera_coordinates(pos, settings.camera_origin)
        screen_coord = world_to_screen_coordinates(camera_coord, width, height)

        radius = max(3, round(math.log(objects[idx].m, 10) / math.log(earth_mass, 10) * 10))

        if width > screen_coord[0] > 0 and height > screen_coord[1] > 0:
            pygame.draw.circle(screen, (255, 255, 255), screen_coord, radius)

    pygame.display.flip()


