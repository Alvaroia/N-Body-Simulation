from body import Body
from settings import Settings
from frames import *
import numpy as np


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
