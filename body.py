import numpy as np

class Body:
    """ Class that represent a body in space"""

    """ Gravitational constant """
    G: float = 6.674 * 10**-11

    def __init__(self, mass, position, initial_velocity):
        self.m = mass
        self.r = position
        self.v = initial_velocity

    def compute_aceleration(self, other_body) -> float:
        # object to object vector
        vect = self.r - other_body.r

        # Distant planet - object
        R = np.linalg.norm(vect)

        # unit vector u
        u = vect / R

        # Aceleration toward the other body
        g = -self.G * other_body.m / (R**2) * u

        return g

    def update_velocity(self, g: float, delta_t: float):
        self.v = self.v + g * delta_t

    def update_position(self, delta_t: float):
        self.r = self.r + self.v * delta_t


def update_bodies(objects: list, delta_t: float, n_steps: int) -> list:
    """ Physics computation of orbit using Semi Implicit Euler (https://gafferongames.com/post/integration_basics/)"""
    
    n_bodies: int = len(objects)

    # dims [body] x [x, y] x [t] (2D coordinates)
    position_list = [np.empty((0, 2))] * n_bodies

    # save initial positions
    for i in range(n_bodies):
        position_list[i] = np.append(position_list[i], [[objects[i].r[0], objects[i].r[1]]], axis=0)

    for i in range(n_steps):

        for object in objects:

            acceleration = np.array([0, 0])

            for other_object in objects:
                if other_object is not object:
                    # Obtain the acceleration result of the influence of the other bodies
                    acceleration = acceleration + object.compute_aceleration(other_object)

            object.update_velocity(acceleration, delta_t)

        # we need to compute the position after updating all velocities 
        # in order to not change the computation of next bodies velocities
        for k, object in enumerate(objects):

            object.update_position(delta_t)

            position_list[k] = np.append(position_list[k], [[objects[k].r[0], objects[k].r[1]]], axis=0)

    return position_list
