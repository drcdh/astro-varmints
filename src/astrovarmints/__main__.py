import logging
from time import sleep

import sense_hat as SH

from . import game
from .game import Direction
from .game.common import APP_NAME

logger = logging.getLogger(f"{APP_NAME}")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f"{APP_NAME}.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("Instantiating SenseHat")
sense = SH.SenseHat()  # This will be overwritten if we use sense_emu
logger.info("set_imu_config")
sense.set_imu_config(True, True, True)


def play_game():
    logger.info("Instantiating game")
    G = game.Game(sense.set_pixel, sense.clear, sense.show_message)
    logger.info("Setting joystick callbacks")

    def event_check(event):
        # We only care about presses, not holds or releases
        return event.action == SH.stick.ACTION_PRESSED

    sense.stick.direction_up = G.get_callback(event_check, Direction.UP)
    sense.stick.direction_left = G.get_callback(event_check, Direction.LEFT)
    sense.stick.direction_down = G.get_callback(event_check, Direction.DOWN)
    sense.stick.direction_right = G.get_callback(event_check, Direction.RIGHT)
    sense.stick.direction_middle = G.get_callback(event_check)
    logger.info("Running game")
    G.run()
    logger.info("Game over, as in the program is finished")


if __name__ == "__main__":
    from sys import argv
    if len(argv) > 1 and argv[1] == "emu":
        import sense_emu as SE
        sense = SE.SenseHat()
    play_game()
