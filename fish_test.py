from shapes import Circle, Dot, Line
import pygame
import sys
from colors import *

# Define the screen size
screen_size = screen_width, screen_height = 1080, 720

# Define fps limit
FPS = 30

# Define cursor type
cursor = pygame.cursors.broken_x

# Setting display and getting the surface object
pygame.init()
pygame.mouse.set_cursor(cursor)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
circles = []
for i in range(3):
    circles.append(Circle((250,100*i), 20, white, 5))
my_line = Line((100,100), (300,300), 5)

def main():

    my_circle = Circle((250, 250), 20, white, 0)

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
        #my_circle.display()
        my_line.display()

        for i, circle in enumerate(circles):
            circle.center = tuple(a+20*i for a in mouse_pos)
            circle.display()

        # Display everything in the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()