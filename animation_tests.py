import pygame
import sys
from colors import *
from shapes import *
from dynamics import *

# Define the screen size
screen_size = screen_width, screen_height = 1080, 720

# Define fps limit
FPS = 30

# Setting display and getting the surface object
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Define shapes
my_circle = Circle((400, 350), 20, dark_green, 0)
my_circle2 = Circle((400, 350), 20, dark_blue, 0)

# Define cursor type
cursor = pygame.cursors.diamond
pygame.mouse.set_cursor(cursor)

mouse_pos_array = np.zeros((2), dtype=tuple)
circle_pos_array = np.zeros((2), dtype=tuple)

# Define control parameters
constants = f, zeta, r = [1, 0.5, 2]
constants2 = f, zeta, r = [1, 0.5, 2]

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
    my_circle.center, my_circle.vel = SecondOrderDynamics(mouse_pos_array, my_circle.center, my_circle.vel, constants, 1/FPS)
    
    # Calculate second circle position and velocity based on first circle
    circle_pos_array = np.roll(circle_pos_array, -1)
    circle_pos_array[-1] = np.array(my_circle.center)
    my_circle2.center, my_circle2.vel = SecondOrderDynamics(circle_pos_array, my_circle2.center, my_circle2.vel, constants2, 1/FPS)

    # Clear the screen
    screen.fill(black)

    # Draw circle in calculated position and update
    my_circle2.display()
    my_circle.display()

    # Display everything in the screen
    pygame.display.flip()
    