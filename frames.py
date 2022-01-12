import numpy as np

max_num = 42371000 * 4/3  # (radio_tierra + radio geo) * 4/3


def world_to_camera_coordinates(world_coordinates, camera_origin):
    return world_coordinates - camera_origin


def camera_to_world_coordinates(camera_coord, camera_origin):
    return camera_coord + camera_origin


def screen_to_camera_coordinates(screen_coordinates, width: int, height: int):
    x = screen_coordinates[0]
    y = screen_coordinates[1]

    camera_x = x / width * 2*max_num - max_num
    camera_y = y / height * 2*max_num - max_num

    return [camera_x, camera_y]


def camera_to_screen_coordinates(world_coordinates, width: int, height: int) -> list:
    """ Can be used as camera to screen coordinates too (I think)"""

    min_num = -max_num

    norm_coord = (world_coordinates - min_num) / (max_num - min_num)  # [0, 1]

    screen_coordinates = [round(norm_coord[0] * width), round(norm_coord[1] * height)]  # [0, width]

    return screen_coordinates


def screen_to_world_coordinates(screen_coordinates, width: int, height: int) -> list:

    x = screen_coordinates[0]
    y = screen_coordinates[1]

    world_x = x / width * 2*max_num - max_num
    world_y = y / height * 2*max_num - max_num

    return [world_x, world_y]


def screen_to_world_vector(screen_vector, width, height):
    transformation_matrix = np.array(
        [max_num/width, 0],
        [0, max_num/height]
    )

    return screen_vector * transformation_matrix


def world_to_screen_vector(world_vector, width, height):
    transformation_matrix = np.array(
        [width/max_num, 0],
        [0, height/max_num]
    )

    return world_vector * transformation_matrix


def world_to_screen_coordinates(world_coordinates, settings):

    camera_coord = world_to_camera_coordinates(world_coordinates, settings.camera_origin)
    screen_coord = camera_to_screen_coordinates(camera_coord, settings.width, settings.height)

    return screen_coord
