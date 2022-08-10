import logging

from .common import *

logger = logging.getLogger(f"{APP_NAME}.{__name__}")


def _move(baddy, d):
    logger.debug(f"{baddy} moving {d}")
    baddy.x, baddy.y = stay_onscreen(*adjacent_pixel(baddy.x, baddy.y, d))


def move_up(baddy, player_pos, new_baddy_fn):
    _move(baddy, D.UP)


def move_left(baddy, player_pos, new_baddy_fn):
    _move(baddy, D.LEFT)


def move_down(baddy, player_pos, new_baddy_fn):
    _move(baddy, D.DOWN)


def move_right(baddy, player_pos, new_baddy_fn):
    _move(baddy, D.RIGHT)


def move_forward(baddy, player_pos, new_baddy_fn):
    _move(baddy, baddy.d)


def _shoot(baddy, new_baddy_fn, d):
    logger.debug(f"{baddy} shooting {d}")
    new_baddy_fn(*adjacent_pixel(baddy.x, baddy.y, d))


def shoot_up(baddy, player_pos, new_baddy_fn):
    _shoot(baddy, new_baddy_fn, D.UP)


def shoot_left(baddy, player_pos, new_baddy_fn):
    _shoot(baddy, new_baddy_fn, D.LEFT)


def shoot_down(baddy, player_pos, new_baddy_fn):
    _shoot(baddy, new_baddy_fn, D.DOWN)


def shoot_right(baddy, player_pos, new_baddy_fn):
    _shoot(baddy, new_baddy_fn, D.RIGHT)
