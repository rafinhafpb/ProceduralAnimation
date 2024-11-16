import pygame
import sys
from colors import *
from shapes import Circle, Dot

# Define the screen size
screen_size = screen_width, screen_height = 1080, 720

# Define fps limit
FPS = 30

# Setting display and getting the surface object
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

def SecondOrderDynamics(x_pos, y_pos, y_vel, constants, T):
    # Compute k constants in function of f, zeta and r
    k1 = constants[1] / (np.pi * constants[0])
    k2 = 1 / ((2 * np.pi * constants[0])**2)
    k3 = (constants[2] * constants[1]) / (2 * np.pi * constants[0])
    k2_stable = max(k2, 1.1 * constants[0] * ((T**2)/4 + T*k1/2))   # Clamp k2 to guarantee stability

    # Estimate velocity of x
    x_vel = (x_pos[-1] - x_pos[0]) / T

    # Normalize or dampen k3 contribution
    k3_contrib = k3 * x_vel / (1 + np.abs(x_vel))

    # Estimate next y position and velocity
    next_y_pos = y_pos + T*y_vel
    next_y_vel = y_vel + T*(x_pos[-1] + k3_contrib - next_y_pos - k1*y_vel)/k2_stable

    return next_y_pos, next_y_vel

# Define shapes
my_circle = Circle((400, 350), 20, dark_green, 0)
my_dot = Dot((350, 100), blue)

# Define cursor type
cursor = pygame.cursors.diamond
pygame.mouse.set_cursor(cursor)

mouse_pos_array = np.array([tuple((0, 0)), tuple((0, 0))])
circle_vel = circle_vel_x, circle_vel_y = [0, 0]
constants = f, zeta, r = [1, 0.5, 2]

while True:
    #Limit FPS
    clock.tick(FPS)

    # Condition to clase the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse position
    mouse_pos = np.array(pygame.mouse.get_pos())
    mouse_pos_array = np.roll(mouse_pos_array, -1)
    mouse_pos_array[-1] = mouse_pos

    # Calculate circle position and velocity
    circle_center_x, circle_vel_x = SecondOrderDynamics(mouse_pos_array[:, 0], np.array(my_circle.center)[0], np.array(circle_vel_x), constants, 1/FPS)
    circle_center_y, circle_vel_y = SecondOrderDynamics(mouse_pos_array[:, 1], np.array(my_circle.center)[1], np.array(circle_vel_y), constants, 1/FPS)

    # Clear the screen
    screen.fill(black)

    # Draw circle in calculated position and update
    my_circle.center = circle_center_x, circle_center_y
    my_circle.display()

    # Display everything in the screen
    pygame.display.flip()
    