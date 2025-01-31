import math

class Axis():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def __add__(self, other):
        result = Axis()
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result

    def __mul__(self, other):
        result = Axis()
        result.x = self.x * other
        result.y = self.y * other
        return result

    def __truediv__(self, other):
        result = Axis()
        result.x = self.x / other
        result.y = self.y / other
        return result
    
    def __sub__(self, other):
        result = Axis()
        result.x = self.x - other.x
        result.y = self.y - other.y
        return result
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def unit(self):
        return self / self.magnitude()
    
    def unit_self(self):
        resultant = self.magnitude()
        self.x /= resultant
        self.y /= resultant

    def zero_self(self):
        self.x = 0
        self.y = 0

class Point():
    def __init__(self):
        self.pos = Axis()
        self.vel = Axis()
        self.acc = Axis()
