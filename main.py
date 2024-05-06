from player import Player
from constants import Dir, Window, MOUSE
from contexts import RoomManager
import pygame
from pygame.event import Event
from subtitles import Subtitle

CLOCK = pygame.time.Clock()
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.game_running = True
        self.screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
        self.rm = RoomManager()
        self.player = Player(self.rm.context)
        self.subtitle = Subtitle("Interact", (200, 200))

    def mainloop(self):
        self.keyDown = False
        self.keys_are_enabled = True

        while self.game_running:
            CLOCK.tick(FPS) # puts the correct screen here
            for event in pygame.event.get():
                self.handle_event(event)
            if self.keyDown:
                self.on_hold()
            current_frame = self.player.animation
            self.screen.blit(self.rm.current_background, (0, 0))
            self.screen.blit(current_frame, self.player.location) # will place the character onto the screen at location
            self.prompt_location()
            if self.subtitle.show:
                self.screen.blit(self.subtitle.text, self.subtitle.location)
            pygame.display.update()
        pygame.quit()

    def handle_event(self, event: Event):
        if event.type == pygame.QUIT:
            self.game_running = False
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_click(event)
        if self.keys_are_enabled:
            if event.type == pygame.KEYDOWN:
                self.keyDown = True
                self.on_key_press(event)
            elif event.type == pygame.KEYUP and no_keys_pressed():
                self.keyDown = False
                self.on_key_release(event)
            elif event.type == pygame.KEYUP:
                self.player.orientation = get_direction()   
            
    def on_key_press(self, event):
        direction = get_direction()
        self.player.orientation = direction

    def on_key_release(self, event):
        self.player.stop_movement()

    def on_mouse_click(self, event):
        key = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if key[MOUSE.LEFT]:
            if self.interact(pos):
                self.keys_are_enabled = False
                self.player.stop_movement()
            self.keys_are_enabled = True
            self.subtitle.show = False
            
        if key[MOUSE.MIDDLE]:
            ...
        if key[MOUSE.RIGHT]:
            self.keys_are_enabled = False
            self.player.stop_movement()
            self.subtitle.show = True

    def on_hold(self):
        pass

    def interact(self, pos_clicked):
        print(pos_clicked, self.player.location)
        return False
    
    def prompt_location(self):
        prompt_at = self.rm.prompt_location(self.player.raw_location)
        if prompt_at and not self.subtitle.show:
            self.subtitle.show = True
            self.subtitle.location = prompt_at
            self.put_text()
        elif prompt_at:
            self.put_text()
        else:
            self.subtitle.show = False
    
    def put_text(self):
        self.screen.blit(self.subtitle.text, self.subtitle.location)

def get_direction() -> int:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_a]:
            return Dir.UP_LEFT
        if keys[pygame.K_w] and keys[pygame.K_d]:
            return Dir.UP_RIGHT
        if keys[pygame.K_s] and keys[pygame.K_a]:
            return Dir.DOWN_LEFT
        if keys[pygame.K_s] and keys[pygame.K_d]:
            return Dir.DOWN_RIGHT
        if keys[pygame.K_s]:
            return Dir.DOWN
        if keys[pygame.K_w]:
            return Dir.UP
        if keys[pygame.K_d]:
            return Dir.RIGHT
        if keys[pygame.K_a]:
            return Dir.LEFT
        return Dir.NONE

def no_keys_pressed() -> bool:
    return all(key == False for key in pygame.key.get_pressed())
      
if __name__ == "__main__": 
    game = Game()
    game.mainloop()