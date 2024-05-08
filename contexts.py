import pygame
from constants import Window
from player import Player
from planar import Location
from room import MiddleRoom, SideRoom

class RoomManager:
    def __init__(self):
        self.side_room = SideRoom()
        self.middle_room = MiddleRoom()
        self.context = self.side_room
    
    def switch_context(self):
        if self.context == self.side_room:
            self.context = self.middle_room
        elif self.context == self.middle_room:
            self.context = self.side_room
    
    @property
    def current_background(self):
        return self.context.background
    
    def prompt_location(self, location: Location):
        return self.context.in_area_of_interest(location)

