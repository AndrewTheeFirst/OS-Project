class Dir:
    NONE = -1
    DOWN = 0
    DOWN_LEFT = 1
    LEFT = 2
    UP_LEFT = 3
    UP = 4
    UP_RIGHT = 5
    RIGHT = 6
    DOWN_RIGHT = 7
    NEUTRAL = 8

class Window:
    WIDTH = 720
    HEIGHT = 720

class MOUSE:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

class PlayerInfo:
    BASE_PLAYER_SIZE = 16
    PLAYER_SCALE = 4
    PLAYER_SIZE = BASE_PLAYER_SIZE * PLAYER_SCALE