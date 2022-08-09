#!/usr/bin/python3.7

import logging
from time import sleep

import sense_hat as SH

import game
from game import Direction

logger = logging.getLogger("game_app")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("game.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("Instantiating SenseHat")
sense = SH.SenseHat()
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


if __name__ == "__main__":
    play_game()
