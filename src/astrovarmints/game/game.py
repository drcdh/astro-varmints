import logging
import random
import time

from . import baddies, player
from .common import *

logger = logging.getLogger(f"{APP_NAME}.{__name__}")


class Game:
    def __init__(self, set_pixel_fn, clear_fn, show_msg_fn):
        self.logger = logging.getLogger(f"{APP_NAME}.{__name__}.{self.__class__.__name__}")
        self.logger.debug("Creating Game instance")
        self._set_pixel_fn = set_pixel_fn
        self._clear_fn = clear_fn
        self._show_msg_fn = show_msg_fn
        self._baddies = []
        self._player = player.Player(DIM // 2, DIM // 2, D.UP)
        self._time_since_new_baddy = 0
        self._time_played = 0

    def _sleep(self, t):
        time.sleep(t)
        self._time_since_new_baddy += t
        self._time_played += t

    def run(self):
        try:
            self._run()
        except KeyboardInterrupt:
            pass
        finally:
            self.logger.info("Game over or something!")
            time.sleep(3)
            self._clear_fn()
            score_msg = f"Score: {len(self._baddies)}, " f"Time: {int(self._time_played)} "
            self.logger.info(score_msg)
            self._show_msg_fn(
                score_msg,
                scroll_speed=0.1,
                text_colour=(100, 30, 40),
                back_colour=(0, 5, 5),
            )
            time.sleep(1)
            self._clear_fn()

    def _run(self):
        while True:
            self._draw()
            if self._check_end_condition():
                self.logger.debug("Got end condition")
                break
            self._maybe_add_new_baddy()
            self._run_baddies()
            self._sleep(0.1)

    @property
    def _new_baddy_time(self):
        # TODO: incorporate some sort of difficulty ramp-up
        return random.randint(30, 60) / 10

    def _maybe_add_new_baddy(self):
        if self._time_since_new_baddy >= self._new_baddy_time:
            self._add_new_baddy()
            self._time_since_new_baddy = 0

    def _add_new_baddy(self, baddy=None):
        # TODO: don't spawn baddies where a baddy already is
        x, y = random.choice(EDGE_PIXELS)
        baddy = baddy or baddies.Baddy(x, y, id_=str(len(self._baddies)))
        self._baddies.append(baddy)
        self.logger.debug(f"New {baddy} at {x}, {y}. Look out!")

    def _run_baddies(self):
        for baddy in self._baddies:
            baddy.take_turn(self._player.body_pixel, self._add_new_baddy)

    def _draw(self):
        self._clear_fn()
        self._player.draw(self._set_pixel_fn)
        for baddy in self._baddies:
            baddy.draw(self._set_pixel_fn)

    def _check_end_condition(self):
        for baddy in self._baddies:
            # breakpoint()
            overlap = get_overlap([(baddy.x, baddy.y)], self._player.pixels)
            if overlap:
                self.logger.debug(f"{baddy} overlaps with Player at {overlap}")
                for _ in range(5):
                    for x, y in overlap:
                        self._set_pixel_fn(x, y, 50, 50, 50)
                    time.sleep(0.2)
                    for x, y in overlap:
                        self._set_pixel_fn(x, y, 200, 0, 0)
                    time.sleep(0.2)
                return True
        else:
            return False

    def get_callback(self, event_check=None, d=None):
        """Get a callback function to set to SenseHat.stick. Use d=None for a middle press."""
        if d:

            def _direction_callback(event):
                self.logger.debug(f"{d} press callback invoked")
                if event_check(event):
                    self.logger.debug(f"{d} press callback passed event_check")
                    self._player.go(d)

            return _direction_callback
        else:

            def _middle_callback(event):
                self.logger.debug("Middle press callback invoked")
                if event_check(event):
                    self.logger.debug("Middle press callback passed event_check")
                    pass  # TODO

            return _middle_callback
