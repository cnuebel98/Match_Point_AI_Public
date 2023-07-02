import pygame

class Button:
    
    def __init__(self, x, y, width, height, buttonText="", color=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.color = color

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
        smallfont = pygame.font.SysFont('Arial', 20) 
        text = smallfont.render(self.buttonText, True , self.color)
        win.blit(text , (self.x , self.y))

    def click(self, event):
        ...

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
        
