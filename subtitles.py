from animations import TextAnimation
from planar import Location, Vector
from constants import PlayerInfo
import pygame

COOL_DOWN = 50
BOUNCE_OFFSET = 3

class Subtitle:
    def __init__(self, text, base_location: tuple[int, int], scale = 2):
        ta = TextAnimation(scale)
        self.prev_ticks = pygame.time.get_ticks()
        self.text = ta.makeText(text)
        self.center_vector = Vector((self.text.get_width()) // 2 - PlayerInfo.PLAYER_SIZE, self.text.get_height())
        self.location = base_location
        self.frame = 0
        self.show = False
        self.delta_frame = 1

    @property
    def location(self) -> tuple[int, int]:
        self._attempt_frame_update()
        
        return (self._location - self.center_vector + Vector(0, BOUNCE_OFFSET) * self.frame).components

    @location.setter
    def location(self, location: tuple[int, int]) -> None:
        self._location = Location(location)
    
    def _attempt_frame_update(self) -> None:
        updated_ticks = pygame.time.get_ticks()
        if updated_ticks - self.prev_ticks >= COOL_DOWN:
            if self.frame + self.delta_frame > 4:
                self.delta_frame = -1
            elif self.frame + self.delta_frame < 0:
                self.delta_frame = 1
            self.frame += self.delta_frame
            self.prev_ticks = updated_ticks

