from pygame import image, transform, Surface # image modification
from constants import Window
from planar import Location
from abc import ABC, abstractmethod
from constants import PlayerInfo

class Room(ABC):
    def __init__(self):
        self.background: Surface
        self.boundaries: list[tuple[int, int, int, int]]
        self.areas_of_interest: list[tuple[int, int, int, int]]
        self.objects: list[RoomObject]
    
    @abstractmethod
    def prompt_location(self, location):
        ...

    def in_bounds(self, location: Location):
        for object in self.objects:
            if location.isWithinRect(object.boarder):
                return False
        for area in self.boundaries:
            if location.isWithinRect(area):
                return True
        return False

    def near_interest(self, location: Location):
        for area in self.areas_of_interest:
            if location.isWithin(20, area):
                return True
        return False

    def set_background(self, image_src: str):
        background = image.load(image_src)
        background = transform.scale(background, (Window.WIDTH, Window.HEIGHT))
        for object in self.objects:
            background.blit(object.image, object.location, (0, 0, object.actual_width, object.actual_height))
        return background

    def _place_objects(self):
        for object in self.objects:
            self.background.blit(object.image, object.location, (0, 0, object.width, object.height))

class MiddleRoom(Room):
    def __init__(self):
        self.boundaries = [

        ]
        self.areas_of_interest = [
            
        ]
        self.objects = [
            
        ]
        self.background = self.set_background("assets/sample_room.png")

    def prompt_location(self, location):
        ...

class SideRoom(Room):
    def __init__(self):
        self.boundaries = [
            (15, 180 - (PlayerInfo.PLAYER_SIZE * 2) // 3, 700 - PlayerInfo.PLAYER_SIZE, 700 - PlayerInfo.PLAYER_SIZE)
        ]
        self.areas_of_interest = [
            Location(15, 140),
            Location(200, 300)
        ]
        self.objects = [
            RoomObject("assets/chest_1.png", (15, 140), 16, 16, 5),
            RoomObject("assets/chest_1.png", (200, 300), 16, 16, 10)
        ]
        self.background = self.set_background("assets/room.png")
    
    def prompt_location(self, location):
        ...

class RoomObject:
    H_BOARDER_OFFSET = 15
    V_BOARDER_OFFSET = 10
    def __init__(self, image_src, location: tuple[int, int], width: int, height: int, scale):
        self.actual_width = width * scale
        self.actual_height = height * scale
        self.image = self.set_image(image_src, width, height)
        self.location = location
        x, y = self.location
        self.boarder = (x - PlayerInfo.PLAYER_SIZE + RoomObject.H_BOARDER_OFFSET,
                        y - PlayerInfo.PLAYER_SIZE + RoomObject.V_BOARDER_OFFSET,
                        x + self.actual_width - RoomObject.H_BOARDER_OFFSET,
                        y + self.actual_height - (PlayerInfo.PLAYER_SIZE * 5) // 6) # allows for 5/6's of the player to overlap bottom
    
    def set_image(self, image_src, width, height):
        raw_img = image.load(image_src)
        img = Surface((width, height)).convert_alpha()
        img.blit(raw_img, (0, 0), (0, 0, width, height))
        img = transform.scale(img, (self.actual_width, self.actual_height))
        img.set_colorkey((0, 0, 0))
        return img
    