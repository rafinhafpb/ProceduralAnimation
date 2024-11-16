import pygame
from colors import *
from typing import List, Optional

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
            
lizard_shaped = [52, 58, 40, 60, 68, 71, 65, 50, 28, 15, 11, 9, 7, 7]
fish_shaped = [30, 40, 35, 32, 30, 25, 20, 10, 10]
cobra_shaped = [25, 30, 25, 24, 22, 20, 18, 16, 14, 12, 11, 10, 9, 8, 7, 6, 5, 4]
    