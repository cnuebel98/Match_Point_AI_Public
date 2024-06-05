import pygame

class Button:
    '''This class can create a button object for the main loop with 
    width height and test as well as button collision with the curser'''
    def __init__(self, x, y, width, height, buttonText="", colour=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.colour = colour

    def draw(self, win, colour):
        pygame.draw.rect(win, colour, 
                         (self.x, self.y, self.width, self.height))
        smallfont = pygame.font.SysFont('Arial', 30, bold=True, italic=False) 
        text = smallfont.render(self.buttonText, True , self.colour)
        win.blit(text, (self.x, self.y))

    def update_text(self, text, win, colour):
        pygame.draw.rect(win, colour, 
                         (self.x, self.y, self.width, self.height))
        self.buttonText = text
        smallfont = pygame.font.SysFont('Arial', 30, bold=True, italic=False)
        text = smallfont.render(self.buttonText, True , self.colour)
        win.blit(text, (self.x, self.y))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_button_width(self):
        return self.width

    def get_button_height(self):
        return self.height
    
    def check_button_collision(self, mouse_pos):
        if (mouse_pos[0] >= self.x
            and mouse_pos[0] <= self.x + self.width
            and mouse_pos[1] >= self.y
            and mouse_pos[1] <= self.y + self.height):
            return True
        else: return False