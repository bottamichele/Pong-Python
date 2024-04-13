from enum import Enum
from pygame.math import Vector2


class CollisionTypeField(Enum):
    """Collision type between ball and field or paddle and field."""
    NONE = 0        #No collision
    TOP = 1         #Collision at top border
    RIGHT = 2       #Collision at right-side border
    BOTTOM = 3      #Collision at bottom border
    LEFT = 4        #Collision at left-side border


class Field:
    """A playing field of Pong."""

    def __init__(self, position, width, height):
        """Create new playing field.
        
        Parameters
        --------------------
        position: Vector2
            center position of playing field

        width: float
            width of playing field
            
        height: float
            height of playing field"""
        
        self._center_position = position
        self._width = width
        self._height = height

    @property
    def center_position(self):
        return Vector2(self._center_position.x, self._center_position.y)

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
        
    def check_collision_paddle(self, a_paddle):
        """Check if a paddle collides the border of field.
        
        Parameter
        --------------------
        a_paddle: Paddle
            a paddle of Pong
            
        Return
        --------------------
        coll_type: CollisionTypeField
            type of collision between paddle and the border of field"""
        
        coll_type = CollisionTypeField.NONE
        top_point = Vector2(a_paddle.position.x, self._center_position.y + self._height/2)
        bottom_point = Vector2(a_paddle.position.x, self._center_position.y - self._height/2)
        
        #Does paddle collide the top border of field?
        if a_paddle.collider.check_collision_point(top_point):
            coll_type = CollisionTypeField.TOP

            a_paddle.set_position(a_paddle.position.x, self._center_position.y + self._height/2 - a_paddle.height/2)
            a_paddle.velocity = Vector2()
        #Does paddle collide the bottom border of field?
        elif a_paddle.collider.check_collision_point(bottom_point):
            coll_type = CollisionTypeField.BOTTOM

            a_paddle.set_position(a_paddle.position.x, self._center_position.y - self._height/2 + a_paddle.height/2)
            a_paddle.velocity = Vector2()

        return coll_type

    def check_collision_ball(self, ball):
        """Check if ball collides with the border of field.
        
        Parameter
        --------------------
        ball: Ball
            ball of Pong
            
        Return
        --------------------
        coll_type: CollisionTypeField
            type of collision between ball and the border of field"""
        
        coll_type = CollisionTypeField.NONE
        top_point = Vector2(ball.position.x, self._center_position.y + self._height/2)
        bottom_point = Vector2(ball.position.x, self._center_position.y - self._height/2)
        left_point = Vector2(self._center_position.x - self._width/2, ball.position.y)
        right_point =  Vector2(self._center_position.x + self._width/2, ball.position.y)

        #Does ball collide the top border of field?
        if ball.collider.check_collision_point(top_point):
            coll_type = CollisionTypeField.TOP
            ball.set_position(ball.position.x, self._center_position.y + self._height/2 - ball.radius/2)
        #Does paddle collide the bottom border of field?
        elif ball.collider.check_collision_point(bottom_point):
            coll_type = CollisionTypeField.BOTTOM
            ball.set_position(ball.position.x, self._center_position.y - self._height/2 + ball.radius/2)
        #Does paddle collide the right border of field?
        elif ball.collider.check_collision_point(right_point):
            coll_type = CollisionTypeField.RIGHT
            ball.set_position(self._center_position.x + self._width/2 - ball.radius/2, ball.position.y)
        #Does paddle collide the left border of field?
        elif ball.collider.check_collision_point(left_point):
            coll_type = CollisionTypeField.LEFT
            ball.set_position(self._center_position.x - self._width/2 + ball.radius/2, ball.position.y)

        return coll_type