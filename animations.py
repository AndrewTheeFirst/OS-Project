from pygame import image, transform, Surface # image modification
from pygame import time # changing frames
from constants import Dir

COOL_DOWN = 150
LETTER_SIZE = 16
TEXT_CLOSENESS = 10

class CharacterAnimation:
    def __init__(self, scale):
        self.sheet = image.load("assets\\character_sheet.png").convert_alpha()
        self.animations = self._get_animations(scale)
        self.prev_ticks = time.get_ticks()
        self.frame = 0

    def _get_image(self, animation_set: int, frame: int, scale: int, width: int = 16, height: int = 16, color_key: tuple[int, int, int] = (0, 0, 0)) -> Surface:

        # creates a blank surface at the specified size
        image = Surface((width, height)).convert_alpha()

        # pastes the spritesheet onto the blank surface starting at (0, 0) 
        # using area of sheet from (0, 0) -> += (width, height)
        image.blit(self.sheet, (0, 0), (frame * width, animation_set * height, width, height))

        # scales image
        image = transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color_key)
        return image

    def _get_animations(self, scale) -> list[Surface]:
        animation_set = 8
        return [[self._get_image(animation, frame, scale) for frame in range(4)] for animation in range(animation_set)]

    def _attempt_frame_update(self) -> None:
        updated_ticks = time.get_ticks()
        if updated_ticks - self.prev_ticks >= COOL_DOWN:
            if self.frame == 3:
                self.frame = 0
            else:
                self.frame += 1
            self.prev_ticks = updated_ticks

    def get_current_frame(self, direction, moving) -> Surface:
        if moving:
            self._attempt_frame_update()
        if direction == Dir.NEUTRAL:
            return self.animations[Dir.DOWN][self.frame]
        else:
            return self.animations[direction][self.frame]

class TextAnimation:
    def __init__(self, scale = 2):
        self.sheet = image.load("assets\\font.png").convert_alpha()
        self.actual_size = LETTER_SIZE * scale
        self._letters = self._get_letters()

    def _get_image(self, frame, case):
        x_offset = 8
        x2_offset = 20
        y_offset = 7 + 24*case
        image = Surface((LETTER_SIZE, LETTER_SIZE))
        image.blit(self.sheet, (0, 0), (x_offset + x2_offset*frame, y_offset, LETTER_SIZE, LETTER_SIZE))
        image = transform.scale(image, (self.actual_size, self.actual_size))
        return image

    def _get_letters(self):
        return [[self._get_image(letter, case) for letter in range(26)] for case in range(2)]

    def _get_letter(self, letter: str):
        if letter == " ":
            return 
        letters = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
        index = letters.index(letter)
        case = 1
        if index > 25:
            index -= 26
            case = 0
        return self._letters[case][index]
    
    def makeText(self, text: str):
        num_chars = len(text)
        image = Surface((self.actual_size * num_chars, self.actual_size)).convert_alpha()
        for letter_index in range(num_chars):
            image.blit(self._get_letter(text[letter_index]), # gets letter
                        ((self.actual_size - TEXT_CLOSENESS) * letter_index, 0), # sets letter location
                          (0, 0, self.actual_size, self.actual_size)) # gets full letter
        image.set_colorkey((0, 0, 0)) # make transparent
        return image

if __name__ == "__main__":
    import pygame
    width = 500
    height = 500
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    running = True
    ta = TextAnimation()
    screen.fill((20, 20, 20))
    screen.blit(ta.makeText("Andrew"), (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()