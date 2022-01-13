
class Settings:

    def __init__(self, width, height, camera_origin, screen_color):
        self.width = width
        self.height = height
        self.camera_origin = camera_origin
        self.screen_color = screen_color
        self.interface_color = (255, 255, 255)
        self.body_color = (255, 255, 255)

        self.pause_menu = True

        # Input variables
        self.quit = False
        self.mouse_click_down = False
        self.mouse_click_position = (0, 0, 0)
        self.mouse_click_up = False
        self.add_new_planet = False
        self.new_planet_init_pos = (0, 0)

        self.t1 = 0

        # constants
        self.earth_mass = 5.972 * 10 ** 24
        self.geostationary_orbit = 36 * 10 ** 6  # m
        self.earth_radius = 6371000  # m



