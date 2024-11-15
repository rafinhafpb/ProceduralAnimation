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

# Define shapes
my_circle = Circle((400, 350), 20, dark_green, 0)
my_dot = Dot((350, 100), blue)

# Define cursor type
cursor = pygame.cursors.diamond
pygame.mouse.set_cursor(cursor)

while True:
    #Limit FPS
    clock.tick(FPS)

    # Condition to clase the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Clear the screen
    screen.fill(black)

    # draw circle in current mouse position and display
    my_circle.center = mouse_pos
    my_circle.display()

    # Display everything in the screen
    pygame.display.flip()
    