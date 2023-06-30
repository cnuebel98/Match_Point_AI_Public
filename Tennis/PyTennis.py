import pygame
from Score import Player, Match
import Ralley
import Ball
pygame.init()

nadal = Player("Rafael Nadal", 2000)
djokovic = Player("Novak Djokovic", 2000)
test_match = Match(nadal, djokovic)
#test_match.play_match()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyTennis")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 136, 0)
DARK_GREEN = (0, 80, 0)
BLUE = (0, 164, 255)
YELLOW = (255, 255, 0)
GREY = (47, 79, 79)

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
BALL_RADIUS = 10

COURT_HEIGHT = int(0.8*HEIGHT)
COURT_WIDTH = int(0.4615*COURT_HEIGHT)
LINE_WIDTH = 6
SINGLES_LINES_WIDTH = int(0.75*COURT_WIDTH)
TLINE_HEIGHT = int(0.5385*COURT_HEIGHT)
NET_WIDTH = int(1.2*COURT_WIDTH)

class PlayerRect:
    COLOR = BLUE
    # make velocity dependent on the player
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

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

        
def draw(win, players, ball):
    win.fill(DARK_GREEN)
    
    # Outer Lines
    pygame.draw.rect(win, WHITE, (WIDTH//2 - COURT_WIDTH//2, HEIGHT//2 - COURT_HEIGHT//2, COURT_WIDTH, COURT_HEIGHT))
    pygame.draw.rect(win, GREEN, (WIDTH//2 - COURT_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, COURT_WIDTH-2*LINE_WIDTH, COURT_HEIGHT-2*LINE_WIDTH))
    # Single Lines
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - COURT_HEIGHT//2, SINGLES_LINES_WIDTH, COURT_HEIGHT))
    pygame.draw.rect(win, GREEN, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH-2*LINE_WIDTH, COURT_HEIGHT-2*LINE_WIDTH))
    # T Lines horizontal
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - TLINE_HEIGHT//2, SINGLES_LINES_WIDTH, TLINE_HEIGHT))
    pygame.draw.rect(win, GREEN, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH-2*LINE_WIDTH, TLINE_HEIGHT-2*LINE_WIDTH))
    # Middle T Line vertical
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - TLINE_HEIGHT//2, SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2, TLINE_HEIGHT))
    pygame.draw.rect(win, GREEN, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2 - LINE_WIDTH*2, TLINE_HEIGHT-2*LINE_WIDTH))
    # Net
    pygame.draw.rect(win, WHITE, (WIDTH//2 - NET_WIDTH//2, HEIGHT//2 - LINE_WIDTH//2, NET_WIDTH, LINE_WIDTH))    

    for player in players:
        player.draw(win)

    ball.draw(win)

    pygame.display.update()

def handle_player_movement(keys, bottom_player):
    if keys[pygame.K_w] and bottom_player.y - bottom_player.VELOCITY >= 0:
        bottom_player.move_vertical(up=True)
    if keys[pygame.K_s] and bottom_player.y + bottom_player.VELOCITY + bottom_player.height <= HEIGHT:
        bottom_player.move_vertical(up=False)
    if keys[pygame.K_a] and bottom_player.x - bottom_player.VELOCITY >= 0:
        bottom_player.move_horizontal(left=True)
    if keys[pygame.K_d] and bottom_player.x + bottom_player.VELOCITY + bottom_player.width <= WIDTH:
        bottom_player.move_horizontal(left=False)

def handle_ball_movement(keys, ball):
    if keys[pygame.K_UP] and ball.y - ball.VELOCITY >= 0:
        ball.move_vertical(up=True)
    if keys[pygame.K_DOWN] and ball.y + ball.VELOCITY + ball.radius <= HEIGHT:
        ball.move_vertical(up=False)
    if keys[pygame.K_LEFT] and ball.x - ball.VELOCITY >= 0:
        ball.move_horizontal(left=True)
    if keys[pygame.K_RIGHT] and ball.x + ball.VELOCITY + ball.radius <= WIDTH:
        ball.move_horizontal(left=False)
    #print(str(ball.get_X()) + " " + str(ball.get_Y()))


def encode_shot_selection(keys, ball, ralley):
    ball_x = 0
    ball_y = 0
    current_shot = None

    if keys[pygame.K_SPACE]:
        ball_x = ball.get_X()
        ball_y = ball.get_Y()
        current_shot = str(ball_x)
        ralley.update_ralley(current_shot)
        print(ralley.get_ralley())
    


def main():
    run = True
    clock = pygame.time.Clock()

    bottom_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    top_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball = Ball.Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    ralley = Ralley.Ralley()

    while run:
        draw(WIN, [bottom_player, top_player], ball)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break 
        
        keys = pygame.key.get_pressed()
        handle_player_movement(keys, bottom_player)
        handle_ball_movement(keys, ball)
        encode_shot_selection(keys, ball, ralley)
        
    pygame.quit()

if __name__ == "__main__":
        main()