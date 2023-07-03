import pygame
from score import Player, Match
import ralley
import ball
import bot
import button

pygame.init()

nadal = Player("Rafael Nadal", 2000)
djokovic = Player("Novak Djokovic", 2000)
test_match = Match(nadal, djokovic)
#test_match.play_match()

WIDTH, HEIGHT = 720, 720
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
        
def draw(win, players, ball, button):
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

    button.draw(win, GREY)
    ball.draw(win, YELLOW)

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
    # ToDo: change player movement from wasd to ball position dependent
    # User is only allowed to move the ball
    if keys[pygame.K_UP] and ball.y - ball.VELOCITY >= 0:
        ball.move_vertical(up=True)
    if keys[pygame.K_DOWN] and ball.y + ball.VELOCITY + ball.radius <= HEIGHT:
        ball.move_vertical(up=False)
    if keys[pygame.K_LEFT] and ball.x - ball.VELOCITY >= 0:
        ball.move_horizontal(left=True)
    if keys[pygame.K_RIGHT] and ball.x + ball.VELOCITY + ball.radius <= WIDTH:
        ball.move_horizontal(left=False)
    #print(str(ball.get_X()) + " " + str(ball.get_Y()))

def encode_serve(ball, serve_position):

    ball_x = ball.get_X()
    ball_y = ball.get_Y()
    
    # the ball has to be above the net (2D View) and also below the T-Line of 
    # the top half of the court
    if (ball_y <= HEIGHT//2 - BALL_RADIUS
        and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS):
        # Depending on the serve position, the service field switches
        if serve_position == "right":
            # when the ball is in the right 30% of the opponents left service field, 
            # its encoding it to "down the T" -> 6
            if (ball_x <= WIDTH//2 + BALL_RADIUS 
                and ball_x >= WIDTH//2 - 0.3*(SINGLES_LINES_WIDTH//2)):
                return 6
            # when the ball is in the middle 40% of the left service field of the opponent
            # its encoded as a "body serve" -> 5
            elif (ball_x < WIDTH//2 - 0.3*(SINGLES_LINES_WIDTH//2)
                  and ball_x >= WIDTH//2 - 0.7*(SINGLES_LINES_WIDTH//2)):
                return 5
            # when the ball is in the left 30% of the left service field of the opponent
            # its encoded as a "wide serve" -> 4
            elif (ball_x < WIDTH//2 - 0.7*(SINGLES_LINES_WIDTH//2)
                  and ball_x >= WIDTH//2 - (SINGLES_LINES_WIDTH//2) - BALL_RADIUS):
                return 4
        elif serve_position == "left":
            # when the ball is in the left 30% of the opponents right service field, 
            # its encoding it to "down the T" -> 6
            if (ball_x >= WIDTH//2 - BALL_RADIUS 
                and ball_x <= WIDTH//2 + 0.3*(SINGLES_LINES_WIDTH//2)):
                return 6
            # when the ball is in the middle 40% of the right service field of the opponent
            # its encoded as a "body serve" -> 5
            elif (ball_x > WIDTH//2 + 0.3*(SINGLES_LINES_WIDTH//2)
                  and ball_x <= WIDTH//2 + 0.7*(SINGLES_LINES_WIDTH//2)):
                return 5
            # when the ball is in the right 30% of the right service field of the opponent
            # its encoded as a "wide serve" -> 4
            elif (ball_x > WIDTH//2 + 0.7*(SINGLES_LINES_WIDTH//2)
                  and ball_x <= WIDTH//2 + (SINGLES_LINES_WIDTH//2) + BALL_RADIUS):
                return 4
    else: print("Serve is not valid")

def encode_shot_direction(ball):
    ball_x = ball.get_X()
    ball_y = ball.get_Y()

    # The ball has to be above the net (2D view) and also below the baseline of the 
    # opponents field

    if (ball_y <= HEIGHT//2 - BALL_RADIUS
       and ball_y >= HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS):
        # If the ball is to the right of the left singles line and if it is in the left 
        # 30% of the court, then the encoding is 1
        if (ball_x <= WIDTH//2 - 0.2*SINGLES_LINES_WIDTH
            and ball_x >= WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS):
            return 1
        # If the ball is in the middle 40% of the opponents court, encoding is a 2 
        elif (ball_x > WIDTH//2 - 0.2*SINGLES_LINES_WIDTH
            and ball_x < WIDTH//2 + 0.2*SINGLES_LINES_WIDTH):
            return 2
        # If the shot is in the right 30% of the court, encoding is a 3
        elif (ball_x >= WIDTH//2 + 0.2*SINGLES_LINES_WIDTH
              and ball_x <= WIDTH//2 + SINGLES_LINES_WIDTH//2 + BALL_RADIUS):
            return 3
    else: print("Ball is Long")

def encode_shot_depth(ball):
    ball_x = ball.get_X()
    ball_y = ball.get_Y()
    # If the ball is between both single lines left and right, we can start encoding
    # the Ball depth
    if (ball_x <= WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2
        and ball_x >= WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS):
        # if the ball is in the Service field (Above the net and below the T-Line)
        if (ball_y <= HEIGHT//2
            and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS):
            return 7
        # if the ball is between Base and T Line, but closer to T-Line
        elif (ball_y < HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS
              and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 - ((COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)):
            return 8
        # If the ball is between T and Baseline, but closer to the baseline
        elif (ball_y < HEIGHT//2 - TLINE_HEIGHT//2 - ((COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)
              and ball_y >= HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS):
            return 9
    else: print("Ball is Wide (left or right)")


def encode_shot_selection(ball, ralley):
    print("Player")
    current_shot = ""
    old_ralley = ralley
    serve_position = None

    # when there was no stroke in the ralley yet, it has to be a serve
    if old_ralley.get_shot_count() == 0:
        # ToDo switch serve_position according to score
        serve_position = "right"
        current_shot = encode_serve(ball, serve_position)
        ralley.add_shot_to_ralley(current_shot)
    # ToDo encode the other shots after the serve and add them to the ralley
    # but only for every second shot depending on who is serving
    elif old_ralley.get_shot_count() > 0:
        current_shot = current_shot + str(encode_shot_direction(ball)) + str(encode_shot_depth(ball))
        ralley.add_shot_to_ralley(current_shot)
    print(ralley.get_ralley())
    
def main():
    run = True
    clock = pygame.time.Clock()

    bottom_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    top_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    new_ball = ball.Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    new_ralley = ralley.Ralley()
    new_bot = bot.Bot("NumberOne")
    next_button = button.Button(0.05*WIDTH, 0.05*HEIGHT, WIDTH*0.15, HEIGHT*0.05, "NEXT", WHITE)

    #new_bot.import_data()

    while run:
        draw(WIN, [bottom_player, top_player], new_ball, next_button)
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Take turns in getting shots 
                # from the bot and from the users
                # If mouse button is pressed on the Next Button a turn is taken
                if next_button.check_button_collision(mouse_pos):
                    if new_bot.get_turn() == False:
                        encode_shot_selection(new_ball, new_ralley)
                        new_bot.set_turn(True)
                    elif new_bot.get_turn() == True:
                        new_bot.add_random_shot(new_ralley)
                        new_bot.set_turn(False)
    
        # handle_player_movement(keys, bottom_player)
        # Ball movement for the player is done by arrow keys
        handle_ball_movement(keys, new_ball)

        #ToDo: Ball Movement for the Bot must be done automatically
        
    pygame.quit()

if __name__ == "__main__":
        main()