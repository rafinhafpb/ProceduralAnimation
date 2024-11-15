import pygame
import sys
from colors import *

# Define the screen size
screen_size = screen_width, screen_height = 1080, 720

# Define fps limit
FPS = 30

# Setting display and getting the surface object
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

while True:

    clock.tick(FPS)

    # Condition to clase the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)
    pygame.draw.circle(screen, random, (520, 250), 20)

    # Display everything in the screen
    pygame.display.flip()
    