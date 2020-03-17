# constants (we should put these in another file)
INVISIBLE = (111, 111, 0)
WHITE = 255, 240, 200
BLACK = 20, 20, 40
gold = [212, 175, 55]

# Used
WINSIZE = [1500, 840]
WINCENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
OFFSET = [300, 100]
CENTER_COLOR = [200, 0, 0]
CENTER_SIZE = 10
WHEEL_COLOR = [0, 0, 150]
WHEEL_SIZE = 10
GOAL_COLOR = [0, 150, 0]
GOAL_SIZE = 5

FAKE_COLOR = [100, 100, 100]
FAKE_SIZE = CENTER_SIZE / 4

WHEEL_SPEED_INC = 1
XY_TOL = 5
TURN_P = 0.03
SPEED_P = 0.01

# The true measure is 119.2, unless the center of the wheels is not the correct point of measure
L = 120.4
# Radius of the wheels (mm)
R = 32.5

XY_GOAL = "XY_GOAL"
WHEEL_CONTROL = "WHEEL_CONTROL"
