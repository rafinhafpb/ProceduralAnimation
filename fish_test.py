from shapes import Circle, Dot, Line
import pygame
import sys
from colors import *
import math

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

nb_points = 14

my_points = []
body_shape = [52, 58, 40, 60, 68, 71, 65, 50, 28, 15, 11, 9, 7, 7]

for i in range(nb_points):
    my_points.append(Circle([250, 250], body_shape[i], white))

my_dot = Dot([250, 250], blue)

radius = 50

def main():

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

        if (math.dist(my_points[0].center, mouse_pos)) > radius:
            # Compute direction vector and constrain position
            direction = (my_points[0].center - mouse_pos) / math.dist(mouse_pos, my_points[0].center)
            my_points[0].center = mouse_pos + (direction * radius)

            # Do the same for every other point in the body
            for i in range(nb_points-1):
                if (math.dist(my_points[i].center, my_points[i+1].center)) > radius:
                    # Compute direction vector and constrain position
                    direction = (my_points[i+1].center - my_points[i].center) / math.dist(my_points[i].center, my_points[i+1].center)
                    my_points[i+1].center = my_points[i].center + (direction * radius)

        # Clear the screen
        screen.fill(black)

        for i in range(nb_points):
            my_points[i].display()

        # Display everything in the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()