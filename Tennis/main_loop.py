import pygame
import ralley
import ball
import bot
import stat_bot_djokovic
import button
import pandas as pd
import random
import time
import scoring
import constants as const

WIDTH  = const.Dims.WIDTH
HEIGHT = const.Dims.HEIGHT

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyTennis")

FPS = const.Dims.FPS

WHITE = const.Colors.WHITE
BLACK = const.Colors.BLACK
GREEN = const.Colors.GREEN
DARK_GREEN = const.Colors.DARK_GREEN
BLUE = const.Colors.BLUE
YELLOW = const.Colors.YELLOW
GREY = const.Colors.GREY

# US Open Color Scheme:
US_OPEN_GREEN = const.Colors.US_OPEN_GREEN
US_OPEN_BLUE = const.Colors.US_OPEN_BLUE

# Australien Open Color Scheme:
AUSOPEN_COURT_BLUE = const.Colors.AUSOPEN_COURT_BLUE
AUSOPEN_COURT_LIGHTBLUE = const.Colors.AUSOPEN_COURT_LIGHTBLUE
AUSOPEN_LINECOLOR = const.Colors.AUSOPEN_LINECOLOR

# French Open Color Scheme:
CLAY_COURT_COLOR = const.Colors.CLAY_COURT_COLOR

# Wimbledon Grass Color Scheme
WIMBLEDON_GREEN = const.Colors.WIMBLEDON_GREEN

PLAYER_WIDTH = const.Dims.PLAYER_WIDTH
PLAYER_HEIGHT = const.Dims.PLAYER_HEIGHT
BALL_RADIUS = const.Dims.BALL_RADIUS

COURT_HEIGHT = const.Dims.COURT_HEIGHT
COURT_WIDTH = const.Dims.COURT_WIDTH
LINE_WIDTH = const.Dims.LINE_WIDTH
SINGLES_LINES_WIDTH = const.Dims.SINGLES_LINES_WIDTH
TLINE_HEIGHT = const.Dims.TLINE_HEIGHT
NET_WIDTH = const.Dims.NET_WIDTH

TRANSITION_ANIMATION = False

class PlayerRect:
    # ToDo: Make Players circles instead of squares
    COLOR = BLUE
    # ToDo: Make velocity dependent on the player
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
        
def draw(win, players, ball, buttons):
    win.fill(US_OPEN_GREEN)
    
    # Outer Lines
    pygame.draw.rect(win, WHITE, (WIDTH//2 - COURT_WIDTH//2, HEIGHT//2 - COURT_HEIGHT//2, COURT_WIDTH, COURT_HEIGHT))
    pygame.draw.rect(win, US_OPEN_BLUE, (WIDTH//2 - COURT_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, COURT_WIDTH-2*LINE_WIDTH, COURT_HEIGHT-2*LINE_WIDTH))
    # Single Lines
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - COURT_HEIGHT//2, SINGLES_LINES_WIDTH, COURT_HEIGHT))
    pygame.draw.rect(win, US_OPEN_BLUE, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH-2*LINE_WIDTH, COURT_HEIGHT-2*LINE_WIDTH))
    # T Lines horizontal
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - TLINE_HEIGHT//2, SINGLES_LINES_WIDTH, TLINE_HEIGHT))
    pygame.draw.rect(win, US_OPEN_BLUE, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH-2*LINE_WIDTH, TLINE_HEIGHT-2*LINE_WIDTH))
    # Middle T Line vertical
    pygame.draw.rect(win, WHITE, (WIDTH//2 - SINGLES_LINES_WIDTH//2, HEIGHT//2 - TLINE_HEIGHT//2, SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2, TLINE_HEIGHT))
    pygame.draw.rect(win, US_OPEN_BLUE, (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2 - LINE_WIDTH*2, TLINE_HEIGHT-2*LINE_WIDTH))
    # Net
    pygame.draw.rect(win, WHITE, (WIDTH//2 - NET_WIDTH//2, HEIGHT//2 - LINE_WIDTH//2, NET_WIDTH, LINE_WIDTH))    

    for player in players:
        player.draw(win)

    for button in buttons:
        button.draw(win, WHITE)

    ball.draw(win, YELLOW)

    pygame.display.update()

def handle_player_movement(keys, bottom_player):
    # ToDo: change player movement from wasd to ball position dependent
    if keys[pygame.K_w] and bottom_player.y - bottom_player.VELOCITY >= 0:
        bottom_player.move_vertical(up=True)
    if keys[pygame.K_s] and bottom_player.y + bottom_player.VELOCITY + bottom_player.height <= HEIGHT:
        bottom_player.move_vertical(up=False)
    if keys[pygame.K_a] and bottom_player.x - bottom_player.VELOCITY >= 0:
        bottom_player.move_horizontal(left=True)
    if keys[pygame.K_d] and bottom_player.x + bottom_player.VELOCITY + bottom_player.width <= WIDTH:
        bottom_player.move_horizontal(left=False)

def handle_ball_movement(keys, ball):
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

def move_ball_to_pos(ball, ralley, win, TRANSITION_ANIMATION, turn, current_score):
    # makes the ball go to the position, based on the bot shot
    r = ralley.get_ralley()
    series = pd.Series(r)
    RETURN_DEPTH = ["7", "8", "9"]
    DIRECTIONS = ["1", "2", "3"]
    SERVE_DIRECTION = ["4", "5", "6"]
    x_pos = 10
    y_pos = 10

    current_shot = ""
    current_shot = series[len(series)-1]

    # Takes the last shot in the ralley and iterates through the characters in that shot
    # looks at depth of shot first and finds a fitting y position and then the same for 
    # direction and x posititon
    for c in current_shot:
        # The first if statement checks, whose turn in the ralley it is (of top or bottom player)
        # accordingly, the ball is moved to the right side of the court into the correct space
        
        if turn == "bottom":
            # Ball placement for Serve encoding dependet on shot count, and serving player
            if c in SERVE_DIRECTION:
                point_count = scoring.Scoring.get_point_count_per_game(current_score)
                y_pos = random.randint(HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS, HEIGHT//2 - 0.3*TLINE_HEIGHT//2)
                # Serve to the outside
                if c == "4":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(WIDTH//2 - BALL_RADIUS - SINGLES_LINES_WIDTH//2, WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2, WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)

                # Serve to the body    
                elif c == "5":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2, WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2, WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2)
                
                # Serve down the T            
                elif c == "6":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2, WIDTH//2 + BALL_RADIUS)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 - BALL_RADIUS, WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2)
                    
            if c in RETURN_DEPTH:
                if c == "7":
                    y_pos = random.randint(HEIGHT//2 - TLINE_HEIGHT//2, HEIGHT//2 - BALL_RADIUS//2)
                elif c == "8":
                    y_pos = random.randint(HEIGHT//2 - TLINE_HEIGHT//2 - ((COURT_HEIGHT//2 - TLINE_HEIGHT//2)//2), HEIGHT//2 - TLINE_HEIGHT//2)
                elif c == "9":
                    y_pos = random.randint(HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS, HEIGHT//2 - TLINE_HEIGHT//2 - ((COURT_HEIGHT//2 - TLINE_HEIGHT//2)//2))

            if c in DIRECTIONS:
                if c == "1":
                    #print("1")
                    x_pos = random.randint(WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, WIDTH//2 - int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "2":
                    #print("2")
                    x_pos = random.randint(WIDTH//2 - BALL_RADIUS - int(0.2*SINGLES_LINES_WIDTH//2), WIDTH//2 + BALL_RADIUS + int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "3":
                    #print("3")
                    x_pos = random.randint(WIDTH//2 + int(0.2*SINGLES_LINES_WIDTH) + BALL_RADIUS, WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)

            if (y_pos == 10):
                #print("Error in Ball Positioning on y position from bottom player")
                y_pos = random.randint(HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS)
            if (x_pos == 10):
                #print("Error in Ball Positioning on x position from bottom player")
                x_pos = random.randint(WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, WIDTH//2 + SINGLES_LINES_WIDTH//2 + BALL_RADIUS)

        elif turn == "top":
            # Ball placement for Serve encoding dependet on shot count, and serving player
            if c in SERVE_DIRECTION:
                point_count = scoring.Scoring.get_point_count_per_game(current_score)
                y_pos = random.randint(HEIGHT//2 + 0.3*TLINE_HEIGHT//2, HEIGHT//2 + TLINE_HEIGHT//2 + BALL_RADIUS)
                # Serve to the outside
                if c == "4":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2, WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 - BALL_RADIUS - SINGLES_LINES_WIDTH//2, WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2)

                # Serve to the body    
                elif c == "5":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2, WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2, WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2)
                
                # Serve down the T            
                elif c == "6":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(WIDTH//2 - BALL_RADIUS, WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2, WIDTH//2 + BALL_RADIUS)

            if c in RETURN_DEPTH:
                if c == "7":
                    #print("y Pos because of 7")
                    y_pos = random.randint(HEIGHT//2 + BALL_RADIUS, HEIGHT//2 + TLINE_HEIGHT//2)
                elif c == "8":
                    #print("y Pos because of 8")
                    y_pos = random.randint(HEIGHT//2 + TLINE_HEIGHT//2 + BALL_RADIUS, HEIGHT//2 + TLINE_HEIGHT//2 + (COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)
                elif c == "9":
                    #print("y Pos because of 9")
                    y_pos = random.randint(HEIGHT//2 + TLINE_HEIGHT//2 + (COURT_HEIGHT//2-TLINE_HEIGHT//2)//2, HEIGHT//2 + COURT_HEIGHT//2 + BALL_RADIUS)
                    
            if c in DIRECTIONS:
                if c == "1":
                    #print("x Pos because of 1")
                    x_pos = random.randint(WIDTH//2 + int(0.2*SINGLES_LINES_WIDTH) + BALL_RADIUS, WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)
                elif c == "2":
                    #print("x Pos because of 2")
                    x_pos = random.randint(WIDTH//2 - BALL_RADIUS - int(0.2*SINGLES_LINES_WIDTH//2), WIDTH//2 + BALL_RADIUS + int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "3":
                    #print("x Pos because of 3")
                    x_pos = random.randint(WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, WIDTH//2 - int(0.2*SINGLES_LINES_WIDTH//2))
                    
            if (y_pos == 10):
                #print("Error in Ball Positioning on y position from top player")
                y_pos = random.randint(HEIGHT//2 + BALL_RADIUS, HEIGHT//2 + COURT_HEIGHT//2 + BALL_RADIUS)
            if (x_pos == 10):
                #print("Error in Ball Positioning on x position from top player")
                x_pos = random.randint(WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, WIDTH//2 + SINGLES_LINES_WIDTH//2 + BALL_RADIUS)
    
    if TRANSITION_ANIMATION == True:
        # Here the ball transitions to the new position
        x_diff = x_pos - ball.get_X()
        y_diff = y_pos - ball.get_Y()
        x = ball.get_X()
        y = ball.get_Y()
        for i in range(0, 11, 1):
            ball.move_animation_from_A_to_B(x_diff, y_diff, i, x, y)
            ball.draw(win, YELLOW)
            pygame.display.update()
            time.sleep(const.MenuVariables.animation_time)
    else:
        # Here the ball jumps instantly to the new positions
        ball.set_X(x_pos)
        ball.set_Y(y_pos)

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
    current_shot = ""
    old_ralley = ralley
    serve_position = None

    # when there was no stroke in the ralley yet, it has to be a serve
    if old_ralley.get_shot_count() == 0:
        serve_position = "right"
        current_shot = str(encode_serve(ball, serve_position))
        ralley.add_shot_to_ralley(current_shot)
    # Encode the other shots after the serve and add them to the ralley
    # but only for every second shot depending on who is serving
    elif old_ralley.get_shot_count() > 0:
        current_shot = current_shot + str(encode_shot_direction(ball)) + str(encode_shot_depth(ball))
        ralley.add_shot_to_ralley(current_shot)
    
def main_loop():
    run = True
    clock = pygame.time.Clock()
    # Set MANUAL to true to be able to play with arrow keys
    MANUAL = False
    # Set to false to safe time and not display the transition animation of the ball
    TRANSITION_ANIMATION = True

    bottom_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    top_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    new_ball = ball.Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    new_ralley = ralley.Ralley()
    
    # Here the options are displayed to see what kind of game is displayed
    print("Top Bot " + str(const.MenuVariables.top_bot))
    print("Bottom Bot " + str(const.MenuVariables.bottom_bot))
    print("Animation " + str(const.MenuVariables.animation))
    print("Sets to play " + str(const.MenuVariables.sets_to_play))

    # Different classes for Top Bot are initialized depending on the choice in the main menu
    if const.MenuVariables.top_bot == 1:
        top_bot = bot.Bot("Random")
    elif const.MenuVariables.top_bot == 2:
        top_bot = stat_bot_djokovic.Stat_Bot_Djokovic("Djokovic")
    else: top_bot = bot.Bot("Random")

    # Different classes for Bottom Bot are initialized depending on the choice in the main menu
    if const.MenuVariables.bottom_bot == 1:
        bottom_bot = bot.Bot("Random")
    elif const.MenuVariables.bottom_bot == 2:
        bottom_bot = stat_bot_djokovic.Stat_Bot_Djokovic("Djokovic")
    else: bottom_bot = bot.Bot("Random")

    next_button = button.Button(0.05*WIDTH, 0.05*HEIGHT, WIDTH*0.2, HEIGHT*0.05, "NEXT", BLACK)
    score_text_field = button.Button(0.05*WIDTH, 0.15*HEIGHT, WIDTH*0.2, HEIGHT*0.05, "0-0", BLACK)
    new_score = scoring.Scoring(0, 0, 0, 0, 0, 0, "bottom_player")

    # the bottom player always starts the first game in the first set of the match
    new_score.set_serving_player(1) # 1 for Bottom player, 2 for top player
    new_ball.reset_ball(new_score.get_serving_player(), new_ralley.get_shot_count())
   
    while run:
        draw(WIN, [bottom_player, top_player], new_ball, [next_button, score_text_field])
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Take turns in getting shots from the bot and from the users
                # If mouse button is pressed on the Next Button a turn is taken
                if next_button.check_button_collision(mouse_pos):
                    # This if elif statement looks at which player is serving in the game and sets the turn accordingly
                    # before each new ralley, so always the correct player starts the ralley
                    # ToDo: set turn for service for tiebreak
                    if new_score.get_serving_player() == 1 and new_ralley.get_shot_count() == 0:
                        top_bot.set_turn(False)
                    elif new_score.get_serving_player() == 2 and new_ralley.get_shot_count() == 0:
                        top_bot.set_turn(True)
                    #print(new_score.get_serving_player())
                    #print(new_ralley.get_shot_count())
                    # If its not the bots turn, take the ball position as shot by the user/by the bottom player
                    if top_bot.get_turn() == False:
                        # This is the manual shot encoding, taking the ball position set by arrow keys into account
                        if MANUAL:
                            encode_shot_selection(new_ball, new_ralley)
                        else:
                            bottom_bot.add_shot(new_ralley)
                            move_ball_to_pos(new_ball, new_ralley, WIN, TRANSITION_ANIMATION, "bottom", new_score)
                        top_bot.set_turn(True)

                    # If its the bots turn, call function that gets the shot from the bot
                    elif top_bot.get_turn() == True:
                        top_bot.add_shot(new_ralley)
                        # Ball Movement is an animated transition
                        move_ball_to_pos(new_ball, new_ralley, WIN, TRANSITION_ANIMATION, "top", new_score)
                        top_bot.set_turn(False)
                    
                    # Here the score is updated, depending on the ralley and the shot count and the turn
                    new_ralley.score_update(new_score, new_ball)
                    score_text_field.update_text(str(new_score.get_score()), WIN, BLACK)

        # ToDo: make player move to the ball (low Priority)
        # Ball movement for the player is done by arrow keys
        # handle_ball_movement(keys, new_ball)
    pygame.QUIT

if __name__ == "__main__":
        main_loop()