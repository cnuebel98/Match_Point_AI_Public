import pygame

class Ball:
    COLOR = (255, 255, 0)
    VELOCITY = 3
    def __init__(self, x , y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), self.radius)    

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
        self.x = x

    def get_Y(self):
        return self.y
    
    def set_Y(self, y):
        self.y = y