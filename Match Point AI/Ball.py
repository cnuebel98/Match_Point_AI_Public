import pygame
import constants as const

class Ball:
    '''This is the ball class where most of the ball movement is done 
    and the reset as well as the transition'''
    COLOUR = const.Colours.YELLOW
    VELOCITY = const.Dims.BALL_VELOCITY
    
    def __init__(self, x , y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win, colour):
        pygame.draw.circle(win, colour, (self.x, self.y), self.radius)    

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

    def move_animation_from_A_to_B(self, x_diff, y_diff, i, x, y):
        # The ball moves from the current location to the next location 
        # for that animation the x and y values along the way are 
        # calculated here
        
        new_x = x + x_diff*(i/10)
        new_y = y + y_diff*(i/10)
        self.set_X(new_x)
        self.set_Y(new_y)

    def reset_ball(self, serving_p, point_count):
        # ball is put behind the baseline of the serving player to the 
        # ad or deuce side according to the points in a game
        if serving_p == 1:
            if point_count % 2 == 0:
                # ball is put to bottom players deuce side
                self.set_X(650)
                self.set_Y(648)
            elif point_count % 2 == 1:
                # ball is put to bottom players ad side
                self.set_X(550)
                self.set_Y(648)
        elif serving_p == 2:
            if point_count % 2 == 0:
                # ball is put to top players deuce side
                self.set_X(550)
                self.set_Y(72)
            elif point_count % 2 == 1:
                # ball is put to top players ad side
                self.set_X(650)
                self.set_Y(72)