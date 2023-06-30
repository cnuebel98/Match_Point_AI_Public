import pygame

class Ball:
    COLOR = (255, 255, 0)
    VELOCITY = 3
    def __init__(self, x , y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)    

    def move_vertical(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def move_horizontal(self, left=True):
        if left:
            self.x -= self.VELOCITY
        else:
            self.x += self.VELOCITY

    def get_X(self):
        return self.x
    
    def set_X(self, x):
        self._x = x

    def get_Y(self):
        return self.y
    
    def set_Y(self, y):
        self._y = y