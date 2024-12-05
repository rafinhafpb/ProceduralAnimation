from shapes import *
from dynamics import *
import pygame
import sys
from colors import *
import math
from scipy.interpolate import interp1d, PchipInterpolator

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
constants = f, zeta, r = [1, 1, 2]    # Define control parameters for animation
# ----------------------- #

for i in range(len(body_shape)):
    my_circles.append(Circle(center_screen, body_shape[i], white, 0))

for i in range(2*len(body_shape) + 4):
    my_dots.append(Dot(center_screen, red))

goal = Circle(center_screen, 5, red, 0)

directions = np.zeros((len(body_shape), 2))
angle_threshold = math.radians(angle_threshold)

def main():
    head_pos_array = np.zeros((2), dtype=tuple)
    angles_array = np.linspace(0, 2*np.pi, 100)

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
        # Get current angle from angle array and roll the intire array
        angle = angles_array[0]
        angles_array = np.roll(angles_array, -1)
        # Calculate the x and y coordinates deslocated by the mouse position and radius 50
        circle_coords = np.array([50*math.cos(angle)+mouse_pos[0], 50*math.sin(angle)+mouse_pos[1]])
        goal.center = mouse_pos
        # Updates the next position for the animal to follow
        head_pos_array = np.roll(head_pos_array, -1)
        head_pos_array[-1] = circle_coords
        
        if (math.dist(my_circles[0].center, mouse_pos)) > radius:
            # Compute direction vector and constrain position
            direction = (circle_coords - my_circles[0].center) / math.dist(circle_coords, my_circles[0].center)
            directions[0] = direction

            # Calculate next head position and velocity
            my_circles[0].center, my_circles[0].vel = SecondOrderDynamics(head_pos_array, my_circles[0].center, my_circles[0].vel, constants, 1/FPS)

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

            # Compute the dots in the right side of the body
            for i, circle in enumerate(my_circles):
                # Compute dots in the head
                if i == 0:
                    dx, dy = directions[0]
                    sides = np.array([-dy, dx]), np.array([dy, -dx])
                    # First dot is the right side of the head
                    my_dots[0].center = circle.center + sides[0] * circle.size

                    # Rotate the vector by 45 degrees
                    rotated_direction = rotate_vector(directions[0], math.pi/4, 1)
                    my_dots[1].center = circle.center + rotated_direction * circle.size

                    # Dot right in front of the direction faced
                    my_dots[2].center = circle.center + directions[0] * circle.size

                    # Rotate the vector by -45 degrees
                    rotated_direction = rotate_vector(directions[0], math.pi/4, -1)
                    my_dots[3].center = circle.center + rotated_direction * circle.size

                    # Last dot is the left side of the head
                    my_dots[4].center = circle.center + sides[1] * circle.size

                # Last dot to contour the tail
                elif i == (len(my_circles)-1):
                    dx, dy = directions[i]
                    my_dots[i + 4].center = circle.center + np.array([dy, -dx]) * circle.size
                    my_dots[i + 5].center = circle.center - directions[i] * circle.size

                # Rest of the body
                else:
                    dx, dy = directions[i]
                    my_dots[i + 4].center = circle.center + np.array([dy, -dx]) * circle.size

            # Compute the dots in the left side of the body
            for i in range(len(my_circles)):
                if i > 0:
                    offset = len(my_circles)
                    # Itearte backards to finish filling the dots array
                    dx, dy = directions[-i]
                    my_dots[i + offset + 4].center = my_circles[-i].center + np.array([-dy, dx]) * my_circles[-i].size

        # Clear the screen
        screen.fill(dark_blue)

        # Draws whole body connecting the dots
        polygon = np.array([dot.center for dot in my_dots])

        # Calculates refined polygon with more points and draw it
        new_polygon = draw_curved_polygon(polygon, 5, method='quadratic')
        pygame.draw.polygon(screen, white, new_polygon)
        pygame.draw.polygon(screen, black, new_polygon, 2)

        # Display mouse position
        goal.display()

        # Display everything in the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()