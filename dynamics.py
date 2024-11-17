import numpy as np
import math

def SecondOrderDynamics(x_pos, y_pos, y_vel, constants, T):
    """
    Computes the second order dynamics of interpolation curves (how one function responds to another) using
    Semi-implicit Euler Mothod.
    ## Parameters
    **x_pos**: *array_like* -> [Xn-1, Xn]\n
    Array of two values representing the last and the current x position (input).\n
    **y_pos**: *tuple* -> [y0, ..., yn]\n
    The current y position (response, or f(x)).\n
    **y_vel**: *tuple* -> [y0, ..., yn]\n
    The current y velocity. Normally computed from a previous SecondOrderDynamics() call, or a numerical value if it's the initial condition.\n
    **constants**: *array_like* -> [f, zeta, r]\n
    Control parameters for desired motion response. \n
    **f** is the natural frequency, and describes the speed at which the system changes to the input.\n
    **zeta** is the damping coeficient, and describes how the system comes to settle at the target. Zeta = 0 makes the sistem oscilate indefinetly.
    Zeta > 1 creates a response with no overshoot. Values between 0 and 1 combines oscilation levels untill settlement.\n
    **r** controls the initial response to the system. When 0, the system takes time to react. When positive, the system reacts immediadly.
    When negative, the system anticipate the motion.\n
    **T**: *float*
    The delta time (interval) between frames or updates.

    ## Returns:
    **next_y_pos**: *tuple*\n
    The next y position calculated. Can be a tuple of single number or more, in case of 2D or 3D spaces.\n
    **next_y_vel**: *tuple*\n
    The next y velocity calculated. Can be a tuple of single number or more, in case of 2D or 3D spaces.
    """
    # Compute k constants in function of f, zeta and r
    k1 = constants[1] / (np.pi * constants[0])
    k2 = 1 / ((2 * np.pi * constants[0])**2)
    k3 = (constants[2] * constants[1]) / (2 * np.pi * constants[0])
    k2_stable = max(k2, 1.1 * constants[0] * ((T**2)/4 + T*k1/2))   # Clamp k2 to guarantee stability

    try:
        if len(y_pos) > 1:
            y_pos = np.array(y_pos)
            y_vel = np.array(y_vel)
            for i in range(len(y_pos)):
                # Estimate array velocity of x
                x_vel[i] = (x_pos[:, i][-1] - x_pos[:, i][0]) / T

                # Normalize or dampen k3 contribution
                k3_contrib = k3 * x_vel[i] / (1 + np.abs(x_vel[i]))

                # Estimate next y array of positions and velocities
                next_y_pos[i] = y_pos[i] + T*y_vel[i]
                next_y_vel[i] = y_vel[i] + T*(x_pos[:, i][-1] + k3_contrib - next_y_pos[i] - k1*y_vel[i])/k2_stable
    except:
        # Estimate velocity of x
        x_vel = (x_pos[-1] - x_pos[0]) / T

        # Normalize or dampen k3 contribution
        k3_contrib = k3 * x_vel / (1 + np.abs(x_vel))

        # Estimate next y position and velocity
        next_y_pos = y_pos + T*y_vel
        next_y_vel = y_vel + T*(x_pos[-1] + k3_contrib - next_y_pos - k1*y_vel)/k2_stable

    return next_y_pos, next_y_vel

def rotate_vector(vector, angle, direction):
    """
    Rotates a vector by a given angle and a direction.
    ## Parameters
    **vector**: *array_like*\n
    The vector to be rotated.\n
    **angle**: *float*\n
    The angle (in radians) the vector will rotate.\n
    **direction**: *int*\n
    1: rotates counterclockwise\n
    -1: rotates clockwise\n
    ## Returns:
    **new_vector**: *ndarray*\n
    The rotated vector.
    """
    # Rotates a vector by a given angle in a direction
    dx, dy = vector
    rotated_dx = dx * math.cos(angle) - dy * direction * math.sin(angle)
    rotated_dy = dx * direction * math.sin(angle) + dy * math.cos(angle)
    new_vector = np.array([rotated_dx, rotated_dy])
    return new_vector