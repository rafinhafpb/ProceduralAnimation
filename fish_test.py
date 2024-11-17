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
my_circles, my_dots = [], []

# Modifiable variables #
radius = 20
angle_threshold = 30
body_shape = cobra_shaped
# ----------------------- #

for i in range(len(body_shape)):
    my_circles.append(Circle(center_screen, body_shape[i], white))

for i in range(2*len(body_shape) + 4):
    my_dots.append(Dot(center_screen, blue))

directions = directions = np.zeros((len(body_shape), 2))
angle_threshold = math.radians(angle_threshold)

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

        if (math.dist(my_circles[0].center, mouse_pos)) > radius:
            # Compute direction vector and constrain position
            direction = (mouse_pos - my_circles[0].center) / math.dist(mouse_pos, my_circles[0].center)
  
            directions[0] = direction
            my_circles[0].center = mouse_pos - direction * radius

            # Do the same for every other point in the body
            for i in range(len(body_shape)-1):
                if (math.dist(my_circles[i].center, my_circles[i+1].center)) > radius:
                    # Compute direction vector and constrain position
                    direction = (my_circles[i].center - my_circles[i+1].center) / math.dist(my_circles[i].center, my_circles[i+1].center)
                    # Compute angle constrain based on threshold
                    cos_angle = np.dot(directions[i], direction)
                    cos_angle = np.clip(cos_angle, -1, 1)
                    angle = math.acos(cos_angle)
                    if angle > angle_threshold:
                        # Calculate the rotation direction (cross product for 2D)
                        cross_prod = np.cross(directions[i], direction)
                        sign = 1 if cross_prod < 0 else -1
                        clamped_direction = rotate_vector(direction, angle-angle_threshold, sign)
                        directions[i+1] = clamped_direction
                        my_circles[i+1].center = my_circles[i].center - clamped_direction * radius
                    else:    
                        directions[i+1] = direction
                        my_circles[i+1].center = my_circles[i].center - direction * radius

            # Compute lateral points of body
            for i, circle in enumerate(my_circles):
                # Compute dots in the head
                if i == 0:
                    # Dot right in front of the direction faced
                    my_dots[-1].center = circle.center + directions[0] * circle.size

                    dx, dy = directions[0]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    my_dots[2*i].center = circle.center + sides[0] * circle.size
                    my_dots[2*i+1].center = circle.center + sides[1] * circle.size

                    # Rotate the vector by 45 degrees
                    rotated_direction = rotate_vector(directions[i], math.pi/4, 1)
                    my_dots[-2].center = circle.center + rotated_direction * circle.size

                    # Rotate the vector by -45 degrees
                    rotated_direction = rotate_vector(directions[i], math.pi/4, -1)
                    my_dots[-3].center = circle.center + rotated_direction * circle.size
                
                # Three dots to contour the tail
                elif i == (len(my_circles)-1):
                    dx, dy = directions[i]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    my_dots[2*i].center = circle.center + sides[0] * circle.size
                    my_dots[2*i+1].center = circle.center + sides[1] * circle.size
                    my_dots[-4].center = circle.center - directions[i] * circle.size

                # Compute dots in the rest of the body
                else:
                    dx, dy = directions[i]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    my_dots[2*i].center = circle.center + sides[0] * circle.size
                    my_dots[2*i+1].center = circle.center + sides[1] * circle.size

        # Clear the screen
        screen.fill(black)

        # Display circles
        for i in range(len(body_shape)):
            my_circles[i].display()

        # Display dots
        for i in range(len(my_dots)):
            my_dots[i].display()

        # Display everything in the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()