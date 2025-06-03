from application import Pong, ControllerType

if __name__ == "__main__":
    game = Pong(controller_2_type=ControllerType.DUELING_DQN_BOT)
    game.run()