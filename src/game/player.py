from .common import *

class Player:
    _INIT_COLOR = (150, 150, 150)

    def __init__(self, x=DIM // 2, y=BOTTOM - 1, d=D.UP):
        self.logger = logging.getLogger(f"{APP_NAME}.{__name__}.{self.__class__}")
        self.logger.debug("Creating Player instance")
        self.x = x
        self.y = y
        self.d = d
        self.colors = {
            "body": (10, 200, 50),
            "face": (10, 100, 20),
            "hand": (10, 100, 20),
        }

    def _delta(self, d=None):
        d = d or self.d
        return delta(d)

    def validate_pos(self):
        pass

    @property
    def body_pixel(self):
        return self.x, self.y

    @property
    def front_pixel(self):
        return adjacent_pixel(self.x, self.y, self.d)

    @property
    def pixels(self):
        pixels = [
            self.body_pixel,
        ]
        pixels.append(self.front_pixel)
        # pixels.append(self.left_pixel)
        # pixels.append(self.right_pixel)
        return pixels

    @property
    def pixel_color(self):
        cover = [
            (self.body_pixel, self.colors["body"]),
        ]
        cover.append((self.front_pixel, self.colors["face"]))
        # cover.append((self.left_pixel, self.colors["hand"]))
        # cover.append((self.right_pixel, self.colors["hand"]))
        return cover

    def draw(self, set_pixel_fn):
        """set_pixel_fn should have signature (x, y, *args)"""
        for (x, y), color in self.pixel_color:
            set_pixel_fn(x, y, *color)

    def move_forward(self, n=1):
        self.logger.debug("Player is trying to move forward")
        delta_x, delta_y = self._delta(self.d)
        x = self.x + delta_x
        y = self.y + delta_y
        # Check face (not body) position. We're sorta cheating here by assuming the Player shape.
        if (
            x + delta_x < LEFT
            or x + delta_x > RIGHT
            or y + delta_y < TOP
            or y + delta_y > BOTTOM
        ):
            self.logger.debug("Player can't move forward")
        else:
            self.x = x
            self.y = y
            self.logger.debug(f"Player moved to {x}, {y}")

    def point(self, d):
        self.logger.debug(f"Player is point-ing {d} (was pointing {self.d}")
        self.d = d

    def point_up(self):
        self.point(D.UP)

    def point_left(self):
        self.point(D.LEFT)

    def point_down(self):
        self.point(D.DOWN)

    def point_right(self):
        self.point(D.RIGHT)

    def rotate_left(self):
        self.d = Direction.rotated_left(self.d)

    def go(self, d):
        self.logger.debug(f"Player is go-ing {d}")
        if self.d != d:
            self.point(d)
        else:
            self.move_forward()

