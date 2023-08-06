import math

name = "Alternate"

start_string = name + " started!"

description = "Two alternating colors"

schema = {
    "speed": {
        "value": {"type": "number", "min": 0, "max": 100, "default": 1},
        "user_input": True,
        "required": False,
    },
    "color 1": {
        "value": {"type": "color", "default": (255, 0, 0)},
        "user_input": True,
        "required": False,
    },
    "color 2": {
        "value": {"type": "color", "default": (0, 0, 255)},
        "user_input": True,
        "required": False,
    },
}


def update(lights, step, state):
    for i in range(lights.size):
        if (i + step) % 2 == 0:
            lights.set_pixel(i, *state["color 1"])
        else:
            lights.set_pixel(i, *state["color 2"])
