import torch as tc
import numpy as np

from torch.nn import Module, Sequential, Linear, ReLU

from pygame.math import Vector2

from .controller import Controller, MovingType, PaddlePosition

# ========================================
# ============== DUELING DQN =============
# ========================================

class DuelingDQN(Module):
    """A Dueling Deep Q-Networks which employs only fully connected layers."""

    def __init__(self):
        """Create new dueling DQN."""
        
        super().__init__()

        #Shared hidden layers.
        self._hidden = Sequential()
        self._hidden.append(Linear(12, 256))
        self._hidden.append(ReLU())
        self._hidden.append(Linear(256, 256))
        self._hidden.append(ReLU())

        #Advantage hidden layers.
        self._adv = Sequential()
        self._adv.append(Linear(256, 3))

        #Value hidden layers.
        self._value = Sequential()
        self._value.append(Linear(256, 1))

    def forward(self, x):
        """Process x.
        
        Parameter
        --------------------
        x: tc.Tensor
            a tensor
            
        Return
        --------------------
        y: tc.Tensor
            x processed by dueling DQN"""
        
        x = self._hidden(x)
        v = self._value(x)
        adv = self._adv(x)
        
        return v + adv - adv.mean(dim=1, keepdim=True)

# ========================================
# ======== DUELING DQN CONTROLLER ========
# ========================================

class DuelingDQNController(Controller):
    """A bot controller which uses Dueling DQN trained with self-play."""

    def __init__(self, a_paddle, position, current_game):
        """Create new bot controller which uses Dueling DQN.
        
        Parameters
        --------------------
        a_paddle: Paddle
            a paddle which is played with
            
        position: PaddlePosition
            the position of the paddle which it controls with
            
        current_game: Game
            game session"""

        super().__init__(a_paddle, position)
        self._opponent_paddle = current_game.paddle_1 if position == PaddlePosition.RIGHT else current_game.paddle_2
        self._ball = current_game.ball
        self._field = current_game.field
        
        #Load the model.
        self._model = DuelingDQN()
        self._model.load_state_dict(tc.load("./pong/controller/dueling_dqn.pth"))
        self._model.eval()

    def update(self, delta_time):
        #Helpful functions.
        def normalize_position(a_position, field):
            return Vector2((a_position.x - field.center_position.x) / (field.width/2),
                           (a_position.y - field.center_position.y) / (field.height/2))
        
        def normalize_velocity(a_velocity):
            return a_velocity.normalize() if a_velocity.length_squared() != 0 else Vector2()
        
        #Bot's paddle.
        paddle_velocity = normalize_velocity(self._paddle.velocity)
        paddle_position = normalize_position(self._paddle.position, self._field)

        #Opponent's paddle
        opponent_paddle_velocity = normalize_velocity(self._opponent_paddle.velocity)
        opponent_paddle_position = normalize_position(self._opponent_paddle.position, self._field)

        #Ball.
        ball_velocity = normalize_velocity(self._ball.velocity)
        ball_position = normalize_position(self._ball.position, self._field)

        #Build observation.
        observation = np.array([paddle_position.x, 
                                paddle_position.y, 
                                paddle_velocity.x, 
                                paddle_velocity.y, 
                                opponent_paddle_position.x, 
                                opponent_paddle_position.y,
                                opponent_paddle_velocity.x,
                                opponent_paddle_velocity.y,
                                ball_position.x,
                                ball_position.y,
                                ball_velocity.x,
                                ball_velocity.y], dtype=np.float32)
        if self._position == PaddlePosition.RIGHT:
            observation *= np.array([-1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0], dtype=np.float32)

        #Choose an action.
        q = self._model(tc.Tensor(observation).unsqueeze(0))
        action = q.argmax(dim=1).item()

        #Perform the chosen action.
        self._move_paddle(MovingType(action))