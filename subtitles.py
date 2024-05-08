from animations import TextAnimation
from planar import Location, Vector
from constants import PlayerInfo
import pygame

COOL_DOWN = 50
BOUNCE_OFFSET = 3
TEXT_SCALE = 2

class Subtitle:
    def __init__(self, text, base_location: tuple[int, int]):
        self.ta = TextAnimation(TEXT_SCALE)
        self.prev_ticks = pygame.time.get_ticks()
        self.prev_text = ""
        self.text = text
        self.prev_location = (-1, -1)
        self.location = base_location
        self.frame = 0
        self.show = False
        self.delta_frame = 1

    @property
    def text(self):
        return self._text
    
    @text.setter
    def _text(self, text):
        if text != self.prev_text:
            self._text = self.ta.makeText(text)
            self.center_vector = Vector((self._text.get_width()) // 2, self._text.get_height() // 2)
            self.prev_text = text

    @property
    def location(self) -> tuple[int, int]:
        self._attempt_frame_update()
        return (self._location - self.center_vector + Vector(0, BOUNCE_OFFSET) * self.frame).components

    @location.setter
    def location(self, location: tuple[int, int]) -> None:
        if location != self.prev_location:
            self._location = Location(location)
            self.prev_location = location
    
    def _attempt_frame_update(self) -> None:
        updated_ticks = pygame.time.get_ticks()
        if updated_ticks - self.prev_ticks >= COOL_DOWN:
            if self.frame + self.delta_frame > 4:
                self.delta_frame = -1
            elif self.frame + self.delta_frame < 0:
                self.delta_frame = 1
            self.frame += self.delta_frame
            self.prev_ticks = updated_ticks

