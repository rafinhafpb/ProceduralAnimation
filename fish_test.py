from shapes import *
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
center_screen = np.array(screen.get_size())/2
clock = pygame.time.Clock()

my_points, my_dots = [], []
body_shape = fish_shaped

for i in range(len(body_shape)):
    my_points.append(Circle(center_screen, body_shape[i], white))

for i in range(2*len(body_shape) + 3):
    my_dots.append(Dot(center_screen, blue))

radius = 30
directions = np.zeros((len(body_shape), 2))

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
            directions[0] = direction

            my_points[0].center = mouse_pos + (direction * radius)

            # Do the same for every other point in the body
            for i in range(len(body_shape)-1):
                if (math.dist(my_points[i].center, my_points[i+1].center)) > radius:
                    # Compute direction vector and constrain position
                    direction = (my_points[i+1].center - my_points[i].center) / math.dist(my_points[i].center, my_points[i+1].center)
                    directions[i+1] = direction

                    my_points[i+1].center = my_points[i].center + (direction * radius)
            
            # Compute lateral points of body
            for i, circle in enumerate(my_points):
                if i == 0:
                    dx, dy = directions[0]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    my_dots[2*i].center = circle.center + sides[0] * circle.size
                    my_dots[2*i+1].center = circle.center + sides[1] * circle.size

                    # Rotate the vector by 45 degrees counterclockwise
                    rotated_dx = dx * math.cos(math.pi / 4) - dy * math.sin(math.pi / 4)
                    rotated_dy = dx * math.sin(math.pi / 4) + dy * math.cos(math.pi / 4)

                    rotated_direction = np.array([rotated_dx, rotated_dy])
                    my_dots[-1].center = circle.center + rotated_direction * circle.size
                    my_dots[-2].center = circle.center + directions[0] * circle.size

                    # Rotate the vector by -45 degrees counterclockwise
                    rotated_dx = dx * math.cos(math.pi / 4) + dy * math.sin(math.pi / 4)
                    rotated_dy = - dx * math.sin(math.pi / 4) + dy * math.cos(math.pi / 4)

                    rotated_direction = np.array([rotated_dx, rotated_dy])
                    my_dots[-3].center = circle.center + directions[0] * circle.size
                else:
                    dx, dy = directions[i]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    my_dots[2*i].center = circle.center + sides[0] * circle.size
                    my_dots[2*i+1].center = circle.center + sides[1] * circle.size

        # Clear the screen
        screen.fill(black)

        for i in range(len(body_shape)):
            my_points[i].display()

        for i in range(len(my_dots)):
            my_dots[i].display()

        # Display everything in the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()