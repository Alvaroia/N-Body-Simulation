from body import Body
from body import update_bodies
from settings import Settings
from frames import *
import numpy as np
import pygame
import sys
import copy
import math


def new_body_on_click_position(origin_click_pos, end_click_position,
                               mass: float, settings: Settings):

    line_vect = np.array([end_click_position[0] - origin_click_pos[0],
                          end_click_position[1] - origin_click_pos[1]])

    screen_pos = screen_to_camera_coordinates(origin_click_pos, settings.width, settings.height)
    world_pos = camera_to_world_coordinates(screen_pos, settings.camera_origin)

    r = np.array([world_pos[0], world_pos[1]])
    velocity_vector = line_vect / 50 * 3000  # 50 pixels = 3000 m/s  # TODO: make this screen independent
    new_body = Body(mass, r, velocity_vector)

    return new_body


def handle_menu_events(event, click_pos, button, slider, settings):
    
    if button.rect.collidepoint(click_pos):
        button.hover = True
    else:
        button.hover = False
    
    if event.type == pygame.QUIT:
        settings.quit = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        settings.mouse_click_down = True
        settings.mouse_click_position = click_pos

        if button.hover:
            settings.pause_menu = False
            settings.t1 = pygame.time.get_ticks()

        elif slider.rect.collidepoint(settings.mouse_click_position[0], settings.mouse_click_position[1]):
            slider.enabled = True
        else:
            settings.add_new_planet = True

            settings.new_planet_init_pos = settings.mouse_click_position

    if event.type == pygame.MOUSEBUTTONUP:
        settings.mouse_click_down = False
        settings.mouse_click_up = True
        slider.enabled = False


def update_menu_data(click_pos, objects, button, slider, settings):
    if settings.mouse_click_up:
        settings.mouse_click_up = False
        if settings.add_new_planet:
            # Add new body
            new_object = new_body_on_click_position(settings.new_planet_init_pos, click_pos, slider.value, settings)
            objects.append(new_object)

            settings.add_new_planet = False

    if settings.quit:
        pygame.quit()
        sys.exit()

    if slider.enabled:
        slider.update_cursor_position(click_pos)

    # Simulate n-steps
    simulation_results = []
    if settings.add_new_planet:
        # Simulate trajectory of object
        delta_t = 60  # 1 min
        n_steps = 600

        # Create new body on click position
        simulate_object = new_body_on_click_position(settings.mouse_click_position, click_pos, slider.value, settings)

        # Make a deep copy of body list to simulate into the future
        objects_test = copy.deepcopy(objects)
        objects_test.append(simulate_object)

        # Simulate n_steps * delta_t seconds into the future and return the obtained positions
        simulation_results = update_bodies(objects_test, delta_t, n_steps)

    return simulation_results


def draw_menu(screen, objects, simulation_results, button, slider, settings):
    screen.fill(settings.screen_color)

    button.draw(screen)
    slider.draw(screen)
    draw_planets(objects, screen, settings)
    draw_simulation_results(simulation_results, screen, settings)

    pygame.display.flip()


def draw_simulation_results(simulation_results, screen, settings):

    for idx, obj in enumerate(simulation_results):
        pos = simulation_results[idx][0, :]

        screen_coord = world_to_screen_coordinates(pos, settings)

        # radius = max(3, round(math.log(slider.value, 10) / math.log(earth_mass, 10) * 10))
        #
        # if settings.width > screen_coord[0] > 0 and settings.height > screen_coord[1] > 0:
        #     pygame.draw.circle(screen, (255, 255, 255), screen_coord, radius)

        for step in range(simulation_results[idx].shape[0] - 1):
            pos_t1 = simulation_results[idx][step]

            screen_coord_t1 = world_to_screen_coordinates(pos_t1, settings)

            pos_t2 = simulation_results[idx][step + 1]

            screen_coord_t2 = world_to_screen_coordinates(pos_t2, settings)

            pygame.draw.line(screen, settings.interface_color, screen_coord_t1, screen_coord_t2)


def draw_planets(objects, screen, settings):

    for idx, obj in enumerate(objects):

        screen_coord = world_to_screen_coordinates(obj.r, settings)

        radius = max(3, round(math.log(objects[idx].m, 10) / math.log(settings.earth_mass, 10) * 10))

        if settings.width > screen_coord[0] > 0 and settings.height > screen_coord[1] > 0:
            pygame.draw.circle(screen, settings.body_color, screen_coord, radius)


def handle_simulation_events(event, click_pos, button, slider, settings):

    if event.type == pygame.QUIT:
        settings.quit = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        settings.mouse_click_position = pygame.mouse.get_pos()

        if button.hover:
            settings.pause_menu = True
        elif slider.rect.collidepoint(settings.mouse_click_position[0], settings.mouse_click_position[1]):
            slider.enabled = True
        else:
            settings.add_new_planet = True

            settings.new_planet_init_pos = settings.mouse_click_position

    if event.type == pygame.MOUSEBUTTONUP:
        settings.mouse_click_up = True

        slider.enabled = False


def update_simulation_data(click_pos, objects, start_button, slider, settings):
    # update simulation

    # Add new body
    if settings.mouse_click_up:
        settings.mouse_click_up = False

        if settings.add_new_planet:
            new_body = new_body_on_click_position(settings.new_planet_init_pos, click_pos, slider.value, settings)
            objects.append(new_body)

            settings.add_new_planet = False

    # Simulate next time step
    t2 = pygame.time.get_ticks()
    delta_t = (t2 - settings.t1)
    settings.t1 = t2

    simulation_results = update_bodies(objects, delta_t, 1)

    if slider.enabled:
        slider.update_cursor_position(click_pos)

    if settings.quit:
        pygame.quit()
        sys.exit()

    return simulation_results


def draw_simulation(screen, objects, simulation_results, button, slider, click_pos, settings):
    screen.fill(settings.screen_color)

    slider.draw(screen)
    button.draw(screen)

    if settings.add_new_planet:
        pygame.draw.line(screen, (255, 255, 255), settings.new_planet_init_pos, click_pos)

    for idx, obj in enumerate(simulation_results):

        pos = simulation_results[idx][-1, :]

        screen_coord = world_to_screen_coordinates(pos, settings)

        radius = max(3, round(math.log(objects[idx].m, 10) / math.log(settings.earth_mass, 10) * 10))

        if settings.width > screen_coord[0] > 0 and settings.height > screen_coord[1] > 0:
            pygame.draw.circle(screen, (255, 255, 255), screen_coord, radius)

    pygame.display.flip()