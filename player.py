from constants import Dir, Window
from planar import Location, Vector
from animations import CharacterAnimation
from pygame import Surface
from room import Room

class Player:

    def __init__(self, place: Room):
        self.delta_x = 0
        self.delta_y = 0

        self.place = place
        self._orientation = Dir.DOWN
        self.location = (Window.WIDTH // 2, Window.HEIGHT // 2)
        self._animation = CharacterAnimation()
    
    def set_place(self, place: Room):
        self.place = place    

    @property
    def animation(self) -> Surface:
        self._update_position()
        if self.delta_x == 0 and self.delta_y == 0:
            return self._animation.get_current_frame(self.orientation, False)
        else:
            return self._animation.get_current_frame(self.orientation, True)
    
    @property
    def raw_location(self) -> tuple[int, int]:
        return self._location

    @property
    def location(self) -> tuple[int, int]:
        return self._location.components

    @location.setter
    def location(self, location: tuple[int, int]) -> None:
        self._location = Location(location)

    @property
    def orientation(self) -> None:
        return self._orientation

    @orientation.setter
    def orientation(self, direction: int) -> None:
        if direction != -1:
            self._orientation = direction
            self._set_delta(direction)
    
    def stop_movement(self) -> None:
        self.delta_x = 0
        self.delta_y = 0
        self._animation.frame = 0

    def _set_delta(self, direction, velocity = 3) -> None:
        match(direction):
            case Dir.UP:
                self.delta_x = 0
                self.delta_y = -velocity
            case Dir.UP_LEFT:
                self.delta_x = -velocity
                self.delta_y = -velocity
            case Dir.UP_RIGHT:
                self.delta_x = velocity
                self.delta_y = -velocity
            case Dir.DOWN:
                self.delta_x = 0
                self.delta_y = velocity
            case Dir.DOWN_LEFT:
                self.delta_x = -velocity
                self.delta_y = velocity
            case Dir.DOWN_RIGHT:
                self.delta_x = velocity
                self.delta_y = velocity
            case Dir.LEFT:
                self.delta_x = -velocity
                self.delta_y = 0
            case Dir.RIGHT:
                self.delta_x = velocity
                self.delta_y = 0
            case _:
                self.stop_movement()

    def _update_position(self) -> None:
        for displacement in [Vector(self.delta_x, self.delta_y), Vector(0, self.delta_y), Vector(self.delta_x, 0)]:
            new_location = self._location + displacement
            if self.place.in_bounds(new_location):
                self._location = new_location
                break
    
    

