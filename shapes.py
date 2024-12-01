import pygame
from colors import *
from typing import List, Optional
from scipy.interpolate import make_interp_spline, BSpline

class Circle:
    def __init__(self, center:List[int], size:int, color:List[int], width: Optional[int]=1, velocity:List[int]=[0, 0]) -> None:
        """
        Creates a circle to be used with 'pygame' library.
        ## Atributes:
        **center**: *list* -> (x, y)\n
        The center position of the cicle.

        **size**: *int*\n
        The radius of the circle.

        **color**: *list* -> (0-255, 0-255, 0-255)\n
        The color composing a 1x3 list from 0 to 255.

        **width**: *optional, int*\n
        if = 0, circle will be totally filled.\n
        if none is specified, it will be set to 1.

        **velocity**: *list* -> (x, y)\n
        The velocity of the cicle. Used for animation purposes.

        ## Methods:
        **display**: *None*\n
        Displays the circle in the active surface (screen).
        """
        self.center = center
        self.size = size
        self.color = color
        self.width = width
        self.vel = velocity
        self.screen = pygame.display.get_surface()

    def display(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.size, self.width)

class Dot:
    def __init__(self, center:List[int], color:List[int]) -> None:
        """
        Creates a dot to be used with 'pygame' library.
        ## Atributes:
        **center**: *list* -> (x, y)\n
        The center position of the cicle.

        **color**: *list* -> (0-255, 0-255, 0-255)\n
        The color composing a 1x3 list from 0 to 255.

        ## Methods:
        **display**: *None*\n
        Displays the dot in the active surface (screen).
        """
        self.center = center
        self.color = color
        self.screen = pygame.display.get_surface()

    def display(self):
        pygame.draw.circle(self.screen, self.color, self.center, width=0, radius=2)

class Line:
    def __init__(self, start_pos:List[int], end_pos:List[int], width:Optional[int]=1, color:Optional[List[int]]=(255,255,255)) -> None:
        """
        Creates a line to be used with 'pygame' library.
        ## Atributes:
        **start_pos**: *list* -> (x, y)\n
        The start position of the line.

        **end_pos**: *int*\n
        The ending position of the line.

        **color**: *list* -> (0-255, 0-255, 0-255)\n
        The color composing a 1x3 list from 0 to 255.

        **width**: *optional, int*\n
        if = 0, circle will be totally filled.\n
        if none is specified, it will be set to 1.

        ## Methods:
        **display**: *None*\n
        Displays the circle in the active surface (screen).
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.color = color
        self.screen = pygame.display.get_surface()

    def display(self):
        pygame.draw.line(self.screen, self.color, self.start_pos, self.end_pos, self.width)
        

class Chain:
    def __init__(self, center:List[int], nb_nodes:int, dist:Optional[float]=50, color:Optional[List[int]]=(255,255,255), size:Optional[int]=5) -> None:
        """
        Creates a circle to be used with 'pygame' library.
        ## Atributes:
        **center**: *list* -> (x, y)\n
        The center position of the cicle.

        **size**: *int*\n
        The radius of the circle.

        **color**: *list* -> (0-255, 0-255, 0-255)\n
        The color composing a 1x3 list from 0 to 255.

        **width**: *optional, int*\n
        if = 0, circle will be totally filled.\n
        if none is specified, it will be set to 1.

        ## Methods:
        **display**: *None*\n
        Displays the circle in the active surface (screen).
        """
        self.center = center
        self.nb_nodes = nb_nodes
        self.dist = dist
        self.size = size if size <= dist else dist
        self.color = color
        self.width = 0
        self.screen = pygame.display.get_surface()

    def display(self):
        circle = []
        lines = []
        for i in range(self.nb_nodes):
            circle.append(Circle(self.center, self.size, self.color, self.width))
            circle[0].display()

# Bezier interpolation function
def quadratic_bezier(p0, p1, p2, t):
    """Compute a point on a quadratic Bezier curve."""
    return (
        (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
    )

def lerp(p0, p1, t):
    """Compute a point that lerps between two points p0 and p1."""
    return (
        (1 - t) * p0[0] + t * p1[0],
        (1 - t) * p0[1] + t * p1[1]
    )

def cubic_bezier(p0, p1, p2, p3, t):
    """Compute a point on a cubic Bezier curve (Castejau's Algorithm)."""
    return (
        p0 * (-t**3 + 3*t**2 - 3*t + 1) + p1 * (3*t**3 - 6*t**2 + 3*t) + p2 * (-3*t**3 + 3*t**2) + p3 * (t**3)
    )

# Draw a smooth polygon using Bezier curves
def draw_curved_polygon(points, segments=5, method='cubic'):
    """
    Compute a curved polygon based on the Bézier curve method specified.

    ## Parameters
        **points**: *list* -> (x, y)\n
        The points that constitute the polygon.

        **segments**: *int, optional*\n
        The amount of interpolated points between consecutive 3 (quadratic method) or 4 (cubic method) points.

        **method**: *string, optional* -> 'cubic', 'quadratic'\n
        The method to compute the Bézier curve, either cubic or quadratic.

    """
    num_points = len(points)
    curved_polygon = []
    if method == 'cubic':
        for i in range(0, num_points, 2):
            # Define control points for the curve segment
            p0 = points[i]
            p1 = (points[i] + points[(i + 1) % num_points])/2    # The mean between first and second points
            p2 = (points[i+1] + points[(i + 2) % num_points])/2  # The mean between second and third points
            p3 = points[(i + 2) % num_points] # Wrap around to make it closed

            # Draw the curve between p0 and p1 using p1 as the control point
            for t in range(segments):
                t0 = t / segments
                new_point = cubic_bezier(p0, p1, p2, p3, t0)
                curved_polygon.append(new_point)

    elif method == 'quadratic':
        for i in range(num_points):
            # Define control points for the curve segment
            p0 = points[i]
            p1 = (points[i] + points[(i + 1) % num_points])/2  # The medium point between the two
            p2 = points[(i + 1) % num_points]  # Wrap around to make it closed

            # Draw the curve between p0 and p1 using their mean point as the control point
            for t in range(segments):
                t0 = t / segments
                new_point = quadratic_bezier(p0, p1, p2, t0)
                curved_polygon.append(new_point)
    else:
        print("Invalid Method")

    return curved_polygon

lizard_shaped = [52, 58, 40, 60, 68, 71, 65, 50, 28, 15, 11, 9, 7, 7]
fish_shaped = [34, 40, 43, 42, 33, 32, 30, 25, 19, 17, 16, 9, 7]
cobra_shaped = [24, 30, 26]
cobra_shaped.extend(np.linspace(25, 4, 28))
    
#if __name__ == '__main__':
