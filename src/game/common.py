import enum as _enum

APP_NAME = "astro-varmints"

DIM = 8
# x
LEFT, RIGHT = 0, DIM - 1
# y
TOP, BOTTOM = 0, DIM - 1
# Aliases
T, B, L, R = TOP, BOTTOM, LEFT, RIGHT

EDGE_PIXELS = (
    [(_x, TOP) for _x in range(DIM)]
    + [(LEFT, _y) for _y in range(1, DIM - 1)]
    + [(RIGHT, _y) for _y in range(1, DIM - 1)]
    + [(_x, BOTTOM) for _x in range(DIM)]
)
assert (
    len(EDGE_PIXELS) == DIM * 2 + (DIM - 2) * 2
), f"Why are there {len(EDGE_PIXELS)} edge pixels??"


class Direction(_enum.Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    @classmethod
    def rotated_left(cls, d):
        if d == D.UP:
            return D.LEFT
        elif d == D.LEFT:
            return D.DOWN
        elif d == D.DOWN:
            return D.RIGHT
        elif d == D.RIGHT:
            return D.UP
        else:
            raise ValueError(f"Bad direction {d}")


# Alias for Direction class
D = Direction


def delta(d):
    if d == D.UP:
        return 0, -1
    elif d == D.DOWN:
        return 0, 1
    elif d == D.LEFT:
        return -1, 0
    elif d == D.RIGHT:
        return 1, 0
    else:
        raise ValueError(f"Unknown direction {d}")


def adjacent_pixel(x, y, d):
    delta_x, delta_y = delta(d)
    return x + delta_x, y + delta_y


def stay_onscreen(x, y):
    x = min(x, DIM - 1)
    x = max(0, x)
    y = min(y, DIM - 1)
    y = max(0, y)
    return x, y


def wrap(x, y):
    x %= DIM
    y %= DIM
    return x, y


def get_overlap(A, B):
    return set(A) & set(B)
