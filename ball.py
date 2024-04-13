from pygame.math import Vector2
from box_collider import BoxCollider

class Ball:
    """A ball of Pong."""

    SPEED = 300

    def __init__(self, position, radius):
        """Create new ball.
        
        Parameters
        --------------------
        position: Vector2
            initial position of ball
            
        radius: float
            radius of ball"""
        
        self._position = position
        self.velocity = Vector2()
        self._radius = radius
        self.collider = BoxCollider(Vector2(position.x - radius/2, position.y - radius/2), radius, radius)
        self.last_paddle_collided = None

    @property
    def position(self):
        return Vector2(self._position.x, self._position.y)
    
    @property
    def radius(self):
        return self._radius

    def set_position(self, x, y):
        """Set new position.
        
        Parameters
        --------------------
        x: float
            new position x
            
        y: float
            new position y"""
        
        self._position = Vector2(x, y)
        self.collider.position = Vector2(x - self._radius/2, y - self._radius/2)

    def check_collision_paddle(self, a_paddle):
        """Check if it collides a paddle.
        
        Parameter
        --------------------
        a_paddle: Paddle
            a paddle to check if this ball collides with
            
        Return
        --------------------
        is_collided: bool
            True if this ball and a_paddle collide, False otherwise"""
        
        #
        # Weren't this ball and paddle collided?
        #
        if not self.collider.check_collision(a_paddle.collider):
            return False
        
        #
        # This ball and paddle was collided.
        #

        leftside_paddle_point = a_paddle.position + Vector2(-a_paddle.width/2, 0.0)
        rightside_paddle_point = a_paddle.position + Vector2(a_paddle.width/2, 0.0)
        
        if self.collider.check_collision_point(leftside_paddle_point):
            l = abs(self._position.x + self._radius/2 - leftside_paddle_point.x)
            self.set_position(self._position.x - l, self._position.y)
        elif self.collider.check_collision_point(rightside_paddle_point):
            l = abs(self._position.x - self._radius/2 - rightside_paddle_point.x)
            self.set_position(self._position.x + l, self._position.y)

        return True


    def on_collision_paddle(self, a_paddle):
        """Collision event with a paddle.
        
        Parameter
        --------------------
        a_paddle: Paddle
            a paddle"""
        
        if self.check_collision_paddle(a_paddle):
            self.last_paddle_collided = a_paddle

            dir = (0.85 * Vector2(-self.velocity.x, self.velocity.y) + 0.15 * a_paddle.velocity).normalize()
            self.velocity = Ball.SPEED * dir