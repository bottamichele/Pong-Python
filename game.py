import numpy as np

from math import sqrt
from pygame.math import Vector2
from field import Field, CollisionTypeField
from paddle import Paddle
from ball import Ball

class Game:
    """A game session of Pong."""

    def __init__(self, center_position_field=(0,0), size_field=(700, 400), size_paddle=(10, 60), radius_ball=10, score_goal=11):
        """Create a new game of Pong.
        
        Parameters
        --------------------
        center_position_field: tuple, optional
            center position of field. It is represented as (x_c, y_c) where x_c is x-axis coordinate and 
            y_c is y-axis coordinate of center position of field

        size_field: tuple, optional
            size of field. It is represented as (wf, hf) where wf is width of field and 
            hf is height of field
            
        size_paddle: tuple, optional
            size of paddle. It is represented as (wp, hp) where wp is width of paddle and
            hp is height of paddle

        radius_ball: int, optional
            radius of ball
        """
    
        self.field = Field(Vector2(center_position_field[0], center_position_field[1]), size_field[0], size_field[1])
        self.paddle_1 = Paddle(Vector2(-0.95 * size_field[0]/2 + center_position_field[0], center_position_field[1]), size_paddle[0], size_paddle[1])
        self.paddle_2 = Paddle(Vector2(0.95 * size_field[0]/2 + center_position_field[0], center_position_field[1]), size_paddle[0], size_paddle[1])
        self.ball = Ball(Vector2(0, 0), radius_ball)
        self._score_paddle_1 = 0
        self._score_paddle_2 = 0
        self._score_goal = score_goal
        self._score_done = False

    @property
    def score_paddle_1(self):
        return self._score_paddle_1
    
    @property
    def score_paddle_2(self):
        return self._score_paddle_2

    @property
    def score_goal(self):
        return self._score_goal
    
    def _reset_initial_state(self):
        """Reset initial state of paddles and ball."""

        #
        #Reset initial state of paddles.
        #
        self.paddle_1.set_position(-0.95 * self.field.width/2 + self.field.center_position.x, self.field.center_position.y)
        self.paddle_2.set_position(0.95 * self.field.width/2 + self.field.center_position.x, self.field.center_position.y)

        #
        #Reset initial state of ball.
        #
        self.ball.set_position(self.field.center_position.x, self.field.center_position.y)
        self.ball.last_paddle_collided = None

        # ------------------------------
        rng = np.random.default_rng()
        y_dir = rng.uniform(0.0, 0.5)
        x_dir = sqrt(1 - y_dir**2)
        vel_dir_ball = Vector2(x_dir if rng.uniform() <= 0.5 else -x_dir, y_dir if rng.uniform() <= 0.5 else -y_dir)

        self.ball.velocity = Ball.SPEED * vel_dir_ball

    def start(self):
        """Start game session."""

        self._reset_initial_state()

    def update(self, delta_time):
        """Do update step.
        
        Parameter
        --------------------
        delta_time: float
            delta time"""
        
        #Update position of paddles
        self._update_position_paddle(self.paddle_1, delta_time)
        self._update_position_paddle(self.paddle_2, delta_time)

        #Update position of ball.
        new_pos_ball = self.ball.velocity * delta_time + self.ball.position
        self.ball.set_position(new_pos_ball.x, new_pos_ball.y)
        self.ball.on_collision_paddle(self.paddle_1)
        self.ball.on_collision_paddle(self.paddle_2)
        res_coll_type_ball = self.field.check_collision_ball(self.ball)

        if res_coll_type_ball == CollisionTypeField.TOP or  res_coll_type_ball == CollisionTypeField.BOTTOM:
            self.ball.velocity.y *= -1

        #Update score if needed.
        if res_coll_type_ball == CollisionTypeField.LEFT or res_coll_type_ball == CollisionTypeField.RIGHT:
            self._score_done = True

            #Paddle 1 is assigned one point.
            if res_coll_type_ball == CollisionTypeField.RIGHT and self.ball.last_paddle_collided == self.paddle_1:
                self._score_paddle_1 += 1
            #Paddle 2 is assigned one point.
            elif res_coll_type_ball == CollisionTypeField.LEFT and self.ball.last_paddle_collided == self.paddle_2:
                self._score_paddle_2 += 1

        #Reset initial states if score is done.
        if self._score_done:
            self._reset_initial_state()
            self._score_done = False
        
    def _update_position_paddle(self, a_paddle, delta_time):
        """Update position of a paddle.
        
        Parameter
        --------------------
        a_paddle: Paddle
            a paddle of Pong
            
        delta_time: float
            delta time"""
        
        new_pos_paddle = a_paddle.velocity * delta_time + a_paddle.position
        a_paddle.set_position(new_pos_paddle.x, new_pos_paddle.y)
        self.field.check_collision_paddle(a_paddle)

    def is_ended(self):
        """Chech if this game session is ended.
        
        Return
        --------------------
        is_ended: bool
            True if this game session is ended, False otherwise"""
        
        return self._score_paddle_1 == self._score_goal or self._score_paddle_2 == self._score_goal