import logging
import random
import time

from . import baddy_actions
from .common import *


class Baddy:
    _COLOR = (100, 10, 10)

    def __init__(self, x, y, id_="anon"):
        self.logger = logging.getLogger(
            f"{APP_NAME}.{__name__}.{self.__class__}[{id_}]"
        )
        self.logger.debug(f'Creating Baddy instance "{id_}"')
        self.x = x
        self.y = y
        self.id = id_
        self.birthtime = time.time()
        self.last_turn = self.birthtime

    def __str__(self):
        return f"Baddy[{self.id}]"

    # TODO: have (some) baddies evolve as they age?
    @property
    def age(self):
        return time.time() - self.birthtime

    def take_turn(self, player_pos, new_baddy_fn):
        """new_baddy_fn is so a Baddy can create a new Baddy (like a "bullet")."""
        t = time.time() - self.last_turn
        if t >= random.randint(5, 7):
            random.choice(
                [
                    baddy_actions.move_up,
                    baddy_actions.move_left,
                    baddy_actions.move_down,
                    baddy_actions.move_right,
                    # baddy_actions.shoot_up,
                    # baddy_actions.shoot_left,
                    # baddy_actions.shoot_down,
                    # baddy_actions.shoot_right,
                ]
            )(self, player_pos, new_baddy_fn)
            self.last_turn = time.time()

    def draw(self, set_pixel_fn):
        set_pixel_fn(self.x, self.y, *self._COLOR)
