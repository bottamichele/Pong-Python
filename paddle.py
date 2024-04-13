from pygame.math import Vector2
from box_collider import BoxCollider

class Paddle:
    """A paddle of Pong."""

    SPEED = 150

    def __init__(self, position, width, height):
        """Create a paddle.
        
        Parameters
        --------------------
        position: Vector2
            initial position of paddle
            
        width: float
            width of paddle
            
        height: float
            height of paddle"""

        self._position = position
        self.velocity = Vector2()       
        self._width = width
        self._height = height
        self.collider = BoxCollider(Vector2(position.x - width/2, position.y - height/2), width, height)

    @property
    def position(self):
        return Vector2(self._position.x, self._position.y)
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    def set_position(self, x, y):
        """Set new position.
        
        Parameters
        --------------------
        x: float
            new position x
            
        y: float
            new position y"""
        
        self._position = Vector2(x, y)
        self.collider.position = Vector2(x - self._width/2, y - self._height/2)