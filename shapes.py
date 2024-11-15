import pygame
from colors import *
from typing import List, Optional

class Circle:
    def __init__(self, center:List[int], size:int, color:List[int], width: Optional[int]=1) -> None:
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
        self.size = size
        self.color = color
        self.width = width
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