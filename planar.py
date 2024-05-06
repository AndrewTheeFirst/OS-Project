from math import sqrt

class Planar:
    def __init__(self, arg1: int | tuple, y: int = None):
        if isinstance(arg1, tuple):
            self.x, self.y = arg1
        elif isinstance(arg1, int):
            self.x = arg1
            self.y = y

    @property
    def components(self) -> tuple:
        return (self.x, self.y)

class Location(Planar):
    def __add__(self, vector: 'Vector') -> 'Location':
        x1, y1 = self.components
        x2, y2 = vector.components
        return Location(x1 + x2, y1 + y2)

    def __sub__(self, vector: 'Vector') -> 'Location':
        x1, y1 = self.components
        x2, y2 = vector.components
        return Location(x1 - x2, y1 - y2)
    
    def __eq__(self, other: 'Location') -> bool:
        return isinstance(other, Location) and other.components == self.components
    

    def isWithin(self, units: float, location: 'Location'):
        '''
        >>> Location(5, 1).isWithin(1, Location(6, 1))
        True
        >>> Location(-1, 1).isWithin(2, Location(1, 1))
        True
        >>> Location(2, 1).isWithin(1, Location(6, 1))
        False
        '''
        x1, y1 = self.components
        x2, y2 = location.components
        distance = sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return distance <= units

    def isWithinRect(self, rect: tuple[int, int, int, int]):
        '''
        >>> Location(-1, 1).isWithinRect((-2, 1, -1, 0))
        True
        >>> Location(2, 1).isWithinRect((1, 2, 3, 0))
        True
        >>> Location(5, 1).isWithinRect((6, 2, 8, 0))
        False
        '''
        x, y = self.components
        x1, y1, x2, y2, = rect
        return (min(x1, x2) <= x and x <= max(x1, x2)) and (min(y1, y2) <= y and y <= max(y1, y2))

    def isBetween(self, location1: 'Location', location2: 'Location', restraint = 0.01) -> bool:
        '''
        >>> Location(5, 1).isBetween(Location(4, 1), Location(6, 1))
        True
        >>> Location(3, 2).isBetween(Location(1, 1), Location(5, 3))
        True
        >>> Location(3, 3).isBetween(Location(1, 1), Location(5, 3))
        False
        >>> Location(3, 1).isBetween(Location(1, 1), Location(5, 3))
        False
        '''
        x, y = self.components
        x1, y1 = location1.components
        x2, y2 = location2.components
        res = (((y1 - y2)/(x1 - x2)) * (x - x1) - y + y1)
        return  (res < restraint) and (res > -restraint)\
              and min(x1, x2) - restraint <= x <= max(x1, x2)+ restraint\
              and min(y1, y2)- restraint <= y <= max(y1, y2) + restraint

    def isAbove(self, location: 'Location') -> bool:
        '''
        >>> Location(5, 6).isAbove(Location(5, 5))
        False
        >>> Location(5, 5).isAbove(Location(5, 5))
        False
        >>> Location(5, 4).isAbove(Location(5, 5))
        True
        '''
        y = self.y
        y1 = location.y
        return y < y1

    def isBelow(self, location: 'Location') -> bool:
        '''
        >>> Location(5, 6).isBelow(Location(5, 5))
        True
        >>> Location(5, 5).isBelow(Location(5, 5))
        False
        >>> Location(5, 4).isBelow(Location(5, 5))
        False
        '''
        y = self.y
        y1 = location.y
        return y > y1

    def isLeftOf(self, location: 'Location') -> bool:
        '''
        >>> Location(4, 5).isLeftOf(Location(5, 5))
        True
        >>> Location(5, 5).isLeftOf(Location(5, 5))
        False
        >>> Location(6, 5).isLeftOf(Location(5, 5))
        False
        '''
        x = self.x
        x1 = location.x
        return x < x1

    def isRightOf(self, location: 'Location') -> bool:
        '''
        >>> Location(4, 5).isRightOf(Location(5, 5))
        False
        >>> Location(5, 5).isRightOf(Location(5, 5))
        False
        >>> Location(6, 5).isRightOf(Location(5, 5))
        True
        '''
        x = self.x
        x1 = location.x
        return x > x1

    def __str__(self):
        return f'({self.x}\' {self.y}\'\')'

    def __repr__(self):
        return f'Location({self.x}, {self.y})'

class Vector(Planar):
    def __add__(self, __vector: 'Vector') -> 'Vector':
        x1, y1 = self.components
        x2, y2 = __vector.components
        return Vector(x1 + x2, y1 + y2)

    def __sub__(self, __vector: 'Vector') -> 'Vector':
        x1, y1 = self.components
        x2, y2 = __vector.components
        return Vector(x1 - x2, y1 - y2)

    def __mul__(self, __int: int) -> 'Vector':
        return Vector(self.x * __int, self.y * __int)

    def __neg__(self) -> 'Vector':
        return Vector(-self.x, -self.y)
    
    def __str__(self):
        return f'<{self.x}, {self.y}>'

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

if __name__ == '__main__':
    from doctest import testmod
    testmod()

