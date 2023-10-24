import pygame
import ralley
import ball
import bot
import log
import stat_bot_djokovic
import simpler_stat_bot_djoko
import button
import pandas as pd
import random
import time
import scoring
import constants as const
import ralley_tree
import networkx as nx
import mcts_agent

WIDTH  = const.Dims.WIDTH
HEIGHT = const.Dims.HEIGHT

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyTennis")

FPS = const.Dims.FPS

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
    #COLOUR = const.Colours.BLACK
    # ToDo: Make velocity dependent on the player
    VELOCITY = 4

    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self, win):
        pygame.draw.rect(win, 
                         self.colour, 
                         (self.x, self.y, self.width, self.height))

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
    # US Open Colour Scheme
    if const.MenuVariables.colour_scheme == 1:
        court_colour_inside = const.Colours.US_OPEN_BLUE
        court_colour_outside = const.Colours.US_OPEN_GREEN
        line_colour = const.Colours.WHITE
    # Roland Garros Colour Scheme
    elif const.MenuVariables.colour_scheme == 2:
        court_colour_inside = const.Colours.CLAY_COURT_COLOUR
        court_colour_outside = const.Colours.CLAY_COURT_COLOUR
        line_colour = const.Colours.WHITE
    # AusOpen Colour Scheme
    elif const.MenuVariables.colour_scheme == 3:
        court_colour_inside = const.Colours.AUSOPEN_COURT_BLUE
        court_colour_outside = const.Colours.AUSOPEN_COURT_LIGHTBLUE
        line_colour = const.Colours.AUSOPEN_LINECOLOUR
    # Wimbledon Colour Scheme
    elif const.MenuVariables.colour_scheme == 4:
        court_colour_inside = const.Colours.WIMBLEDON_GREEN
        court_colour_outside = const.Colours.WIMBLEDON_GREEN
        line_colour = const.Colours.WHITE

    win.fill(court_colour_outside)
    
    # Outer Lines
    pygame.draw.rect(win, line_colour, 
                     (WIDTH//2 - COURT_WIDTH//2, 
                      HEIGHT//2 - COURT_HEIGHT//2, 
                      COURT_WIDTH, 
                      COURT_HEIGHT))
    pygame.draw.rect(win, court_colour_inside, 
                     (WIDTH//2 - COURT_WIDTH//2 + LINE_WIDTH, 
                      HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, 
                      COURT_WIDTH-2*LINE_WIDTH, 
                      COURT_HEIGHT-2*LINE_WIDTH))
    # Single Lines
    pygame.draw.rect(win, line_colour, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2, 
                      HEIGHT//2 - COURT_HEIGHT//2, 
                      SINGLES_LINES_WIDTH, 
                      COURT_HEIGHT))
    pygame.draw.rect(win, court_colour_inside, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, 
                      HEIGHT//2 - COURT_HEIGHT//2 + LINE_WIDTH, 
                      SINGLES_LINES_WIDTH-2*LINE_WIDTH, 
                      COURT_HEIGHT-2*LINE_WIDTH))
    # T Lines horizontal
    pygame.draw.rect(win, line_colour, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2, 
                      HEIGHT//2 - TLINE_HEIGHT//2, 
                      SINGLES_LINES_WIDTH,
                      TLINE_HEIGHT))
    pygame.draw.rect(win, court_colour_inside, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, 
                      HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, 
                      SINGLES_LINES_WIDTH-2*LINE_WIDTH, 
                      TLINE_HEIGHT-2*LINE_WIDTH))
    # Middle T Line vertical
    pygame.draw.rect(win, line_colour, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2, 
                      HEIGHT//2 - TLINE_HEIGHT//2, 
                      SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2, 
                      TLINE_HEIGHT))
    pygame.draw.rect(win, court_colour_inside, 
                     (WIDTH//2 - SINGLES_LINES_WIDTH//2 + LINE_WIDTH, 
                      HEIGHT//2 - TLINE_HEIGHT//2 + LINE_WIDTH, 
                      SINGLES_LINES_WIDTH//2 + LINE_WIDTH//2 - LINE_WIDTH*2, 
                      TLINE_HEIGHT-2*LINE_WIDTH))
    # Net
    pygame.draw.rect(win, line_colour, 
                     (WIDTH//2 - NET_WIDTH//2, 
                      HEIGHT//2 - LINE_WIDTH//2, 
                      NET_WIDTH, 
                      LINE_WIDTH))    

    for player in players:
        player.draw(win)

    for button in buttons:
        button.draw(win, const.Colours.WHITE)

    ball.draw(win, const.Colours.YELLOW)

    pygame.display.update()

def handle_player_movement(keys, bottom_player):
    # ToDo: change player movement from wasd to ball position dependent
    if (keys[pygame.K_w] 
        and bottom_player.y - bottom_player.VELOCITY >= 0):
        bottom_player.move_vertical(up=True)
    if (keys[pygame.K_s] 
        and bottom_player.y + bottom_player.VELOCITY 
        + bottom_player.height <= HEIGHT):
        bottom_player.move_vertical(up=False)
    if (keys[pygame.K_a] 
        and bottom_player.x - bottom_player.VELOCITY >= 0):
        bottom_player.move_horizontal(left=True)
    if (keys[pygame.K_d] 
        and bottom_player.x + bottom_player.VELOCITY 
        + bottom_player.width <= WIDTH):
        bottom_player.move_horizontal(left=False)

def handle_ball_movement(keys, ball):
    # User is only allowed to move the ball
    if (keys[pygame.K_UP] 
        and ball.y - ball.VELOCITY >= 0):
        ball.move_vertical(up=True)
    if (keys[pygame.K_DOWN] 
        and ball.y + ball.VELOCITY + ball.radius <= HEIGHT):
        ball.move_vertical(up=False)
    if (keys[pygame.K_LEFT] 
        and ball.x - ball.VELOCITY >= 0):
        ball.move_horizontal(left=True)
    if (keys[pygame.K_RIGHT] 
        and ball.x + ball.VELOCITY + ball.radius <= WIDTH):
        ball.move_horizontal(left=False)

def move_ball_to_pos(ball, ralley, win, TRANSITION_ANIMATION, 
                     turn, current_score):
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

    # Takes the last shot in the ralley and iterates through the
    # characters in that shot, looks at depth of shot first and finds a 
    # fitting y position and then the same for direction and x posititon
    for c in current_shot:
        # The first if statement checks, whose turn in the ralley it is 
        # (of top or bottom player)accordingly, the ball is moved to the 
        # right side of the court into the correct space
        if turn == "bottom":
            # Ball placement for Serve encoding dependet on shot count,
            # and serving player
            if c in SERVE_DIRECTION:
                point_count = scoring.Scoring.get_point_count_per_game(
                    current_score)
                y_pos = random.randint(
                    HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS, 
                    HEIGHT//2 - 0.3*TLINE_HEIGHT//2)
                # Serve to the outside
                if c == "4":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 - BALL_RADIUS - SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)

                # Serve to the body    
                elif c == "5":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2)
                
                # Serve down the T            
                elif c == "6":
                    if point_count % 2 == 0:
                        # bottom player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + BALL_RADIUS)
                    elif point_count % 2 == 1:
                        # bottom player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 - BALL_RADIUS, 
                            WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2)
                    
            if c in RETURN_DEPTH:
                if c == "7":
                    y_pos = random.randint(
                        HEIGHT//2 - TLINE_HEIGHT//2, 
                        HEIGHT//2 - BALL_RADIUS//2)
                elif c == "8":
                    y_pos = random.randint(
                        HEIGHT//2 - TLINE_HEIGHT//2 
                        - ((COURT_HEIGHT//2 - TLINE_HEIGHT//2)//2), 
                        HEIGHT//2 - TLINE_HEIGHT//2)
                elif c == "9":
                    y_pos = random.randint(
                        HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS, 
                        HEIGHT//2 - TLINE_HEIGHT//2 
                        - ((COURT_HEIGHT//2 - TLINE_HEIGHT//2)//2))

            if c in DIRECTIONS:
                if c == "1":
                    x_pos = random.randint(
                        WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, 
                        WIDTH//2 - int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "2":
                    x_pos = random.randint(
                        WIDTH//2 - BALL_RADIUS 
                        - int(0.2*SINGLES_LINES_WIDTH//2), 
                        WIDTH//2 + BALL_RADIUS 
                        + int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "3":
                    x_pos = random.randint(
                        WIDTH//2 + int(0.2*SINGLES_LINES_WIDTH) + BALL_RADIUS, 
                        WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)

            if (y_pos == 10):
                y_pos = random.randint(
                    HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS, 
                    HEIGHT//2 - BALL_RADIUS)
            if (x_pos == 10):
                x_pos = random.randint(
                    WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, 
                    WIDTH//2 + SINGLES_LINES_WIDTH//2 + BALL_RADIUS)

        elif turn == "top":
            # Ball placement for Serve encoding dependet on shot count, 
            # and serving player
            if c in SERVE_DIRECTION:
                point_count = scoring.Scoring.get_point_count_per_game(
                    current_score)
                y_pos = random.randint(
                    HEIGHT//2 + 0.3*TLINE_HEIGHT//2, 
                    HEIGHT//2 + TLINE_HEIGHT//2 + BALL_RADIUS)
                # Serve to the outside
                if c == "4":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 - BALL_RADIUS - SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2)

                # Serve to the body    
                elif c == "5":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + 0.7*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 - 0.7*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2)
                
                # Serve down the T            
                elif c == "6":
                    if point_count % 2 == 0:
                        # top player serves from deuce side
                        x_pos = random.randint(
                            WIDTH//2 - BALL_RADIUS, 
                            WIDTH//2 + 0.3*SINGLES_LINES_WIDTH//2)
                    elif point_count % 2 == 1:
                        # top player serves from the Ad side
                        x_pos = random.randint(
                            WIDTH//2 - 0.3*SINGLES_LINES_WIDTH//2, 
                            WIDTH//2 + BALL_RADIUS)

            if c in RETURN_DEPTH:
                if c == "7":
                    #print("y Pos because of 7")
                    y_pos = random.randint(
                        HEIGHT//2 + BALL_RADIUS, HEIGHT//2 + TLINE_HEIGHT//2)
                elif c == "8":
                    #print("y Pos because of 8")
                    y_pos = random.randint(
                        HEIGHT//2 + TLINE_HEIGHT//2 + BALL_RADIUS, 
                        HEIGHT//2 + TLINE_HEIGHT//2 
                        + (COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)
                elif c == "9":
                    #print("y Pos because of 9")
                    y_pos = random.randint(
                        HEIGHT//2 + TLINE_HEIGHT//2 
                        + (COURT_HEIGHT//2-TLINE_HEIGHT//2)//2, 
                        HEIGHT//2 + COURT_HEIGHT//2 + BALL_RADIUS)
                    
            if c in DIRECTIONS:
                if c == "1":
                    #print("x Pos because of 1")
                    x_pos = random.randint(
                        WIDTH//2 + int(0.2*SINGLES_LINES_WIDTH) + BALL_RADIUS, 
                        WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2)
                elif c == "2":
                    #print("x Pos because of 2")
                    x_pos = random.randint(
                        WIDTH//2 - BALL_RADIUS 
                        - int(0.2*SINGLES_LINES_WIDTH//2), 
                        WIDTH//2 + BALL_RADIUS 
                        + int(0.2*SINGLES_LINES_WIDTH//2))
                elif c == "3":
                    #print("x Pos because of 3")
                    x_pos = random.randint(
                        WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, 
                        WIDTH//2 - int(0.2*SINGLES_LINES_WIDTH//2))
                    
            if (y_pos == 10):
                y_pos = random.randint(
                    HEIGHT//2 + BALL_RADIUS, 
                    HEIGHT//2 + COURT_HEIGHT//2 + BALL_RADIUS)
            if (x_pos == 10):
                x_pos = random.randint(
                    WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS, 
                    WIDTH//2 + SINGLES_LINES_WIDTH//2 + BALL_RADIUS)
    
    if TRANSITION_ANIMATION == True:
        # Here the ball transitions to the new position
        x_diff = x_pos - ball.get_X()
        y_diff = y_pos - ball.get_Y()
        x = ball.get_X()
        y = ball.get_Y()
        for i in range(0, 11, 1):
            ball.move_animation_from_A_to_B(x_diff, y_diff, i, x, y)
            ball.draw(win, const.Colours.YELLOW)
            pygame.display.update()
            time.sleep(const.MenuVariables.animation_time)
    else:
        # Here the ball jumps instantly to the new positions
        ball.set_X(x_pos)
        ball.set_Y(y_pos)

def encode_serve(ball, serve_position):

    ball_x = ball.get_X()
    ball_y = ball.get_Y()
    
    # the ball has to be above the net (2D View) and also below the 
    # T-Line of the top half of the court
    if (ball_y <= HEIGHT//2 - BALL_RADIUS
        and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS):
        # Depending on the serve position, the service field switches
        if serve_position == "right":
            # when the ball is in the right 30% of the opponents left 
            # service field, its encoding it to "down the T" -> 6
            if (ball_x <= WIDTH//2 + BALL_RADIUS 
                and ball_x >= WIDTH//2 - 0.3*(SINGLES_LINES_WIDTH//2)):
                return 6
            # when the ball is in the middle 40% of the left service 
            # field of the opponent its encoded as a "body serve" -> 5
            elif (ball_x < WIDTH//2 - 0.3*(SINGLES_LINES_WIDTH//2)
                  and ball_x >= WIDTH//2 - 0.7*(SINGLES_LINES_WIDTH//2)):
                return 5
            # when the ball is in the left 30% of the left service field 
            # of the opponent its encoded as a "wide serve" -> 4
            elif (ball_x < WIDTH//2 - 0.7*(SINGLES_LINES_WIDTH//2)
                  and ball_x >= WIDTH//2 - (SINGLES_LINES_WIDTH//2) 
                  - BALL_RADIUS):
                return 4
        elif serve_position == "left":
            # when the ball is in the left 30% of the opponents right 
            # service field, its encoding it to "down the T" -> 6
            if (ball_x >= WIDTH//2 - BALL_RADIUS 
                and ball_x <= WIDTH//2 + 0.3*(SINGLES_LINES_WIDTH//2)):
                return 6
            # when the ball is in the middle 40% of the right service 
            # field of the opponent its encoded as a "body serve" -> 5
            elif (ball_x > WIDTH//2 + 0.3*(SINGLES_LINES_WIDTH//2)
                  and ball_x <= WIDTH//2 + 0.7*(SINGLES_LINES_WIDTH//2)):
                return 5
            # when the ball is in the right 30% of the right service 
            # field of the opponent its encoded as a "wide serve" -> 4
            elif (ball_x > WIDTH//2 + 0.7*(SINGLES_LINES_WIDTH//2)
                  and ball_x <= WIDTH//2 + (SINGLES_LINES_WIDTH//2) 
                  + BALL_RADIUS):
                return 4
    else: print("Serve is not valid")

def encode_shot_direction(ball):
    ball_x = ball.get_X()
    ball_y = ball.get_Y()

    # The ball has to be above the net (2D view) and also below the 
    # baseline of the opponents field

    if (ball_y <= HEIGHT//2 - BALL_RADIUS
       and ball_y >= HEIGHT//2 - COURT_HEIGHT//2 - BALL_RADIUS):
        # If the ball is to the right of the left singles line and if it
        #  is in the left 30% of the court, then the encoding is 1
        if (ball_x <= WIDTH//2 - 0.2*SINGLES_LINES_WIDTH
            and ball_x >= WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS):
            return 1
        # If the ball is in the middle 40% of the opponents court, 
        # encoding is a 2 
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
    # If the ball is between both single lines left and right, we can 
    # start encoding the Ball depth
    if (ball_x <= WIDTH//2 + BALL_RADIUS + SINGLES_LINES_WIDTH//2
        and ball_x >= WIDTH//2 - SINGLES_LINES_WIDTH//2 - BALL_RADIUS):
        # if the ball is in the Service field (Above the net and below 
        # the T-Line)
        if (ball_y <= HEIGHT//2
            and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS):
            return 7
        # if the ball is between Base and T Line, but closer to T-Line
        elif (ball_y < HEIGHT//2 - TLINE_HEIGHT//2 - BALL_RADIUS
              and ball_y >= HEIGHT//2 - TLINE_HEIGHT//2 
              - ((COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)):
            return 8
        # If the ball is between T and Baseline, but closer to baseline
        elif (ball_y < HEIGHT//2 - TLINE_HEIGHT//2 
              - ((COURT_HEIGHT//2-TLINE_HEIGHT//2)//2)
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
        current_shot = (current_shot + str(encode_shot_direction(ball)) 
                        + str(encode_shot_depth(ball)))
        ralley.add_shot_to_ralley(current_shot)
    
def tree_update(new_ralley, new_tree, colour):
    '''A new node is added to the tree. When the node with the new shot
    already was played from the current game state, then its not added,
    otherwise its added as a directional graph to the tree'''
    
    # The dictionaries are mapping the shot/colour -> index of the node
    shot_dict = new_tree.get_shot_dict_of_neighbors(
        new_tree.get_active_node())
    colour_dict = new_tree.get_colour_dict_of_neighbors(
        new_tree.get_active_node())
    #print(shot_dict)
    #print(colour_dict)
    
    # Shot in tree boolean is initialized
    shot_in_tree = False
    
    #new_tree.add_node_visit(new_tree.get_active_node())

    # We check wether the new shot is already in the child nodes of the
    # current game state
    if (new_ralley.get_last_shot() in
        new_tree.get_shot_list_of_neighbors(new_tree.get_active_node())):
        # If the shot in the gamestate has already been played, then 
        # that node is being set to active
        # print("Matching shots discovered.")
        index_list = []
        
        # Here we set the node active, where the shot already was played
        for x in new_tree.get_shot_list_of_neighbors(
            new_tree.get_active_node()):
            if (x == new_ralley.get_last_shot()):
                
                # matching shot is the value we are looking for in the
                # shot dict to get the indices
                matching_shot = x
                
                # create an index list with all the indices of the
                # shot_dict, where the value has been found

                index_list = [k for k,v in shot_dict.items() 
                              if v == matching_shot]

                for h in range(len(index_list)):
                    if colour_dict[index_list[h]] == colour:
                        #print(True)
                        shot_in_tree = True
                        new_tree.set_active_node(index_list[h])

    # If the shot has not yet been played in the current Gamestate, it 
    # is added to the parent node
    if shot_in_tree == False:
        node_start = new_tree.get_active_node()
        new_tree.add_new_node(new_tree.get_next_node_index(),
                              node_type="state",
                              colour=colour,
                              shot_string=new_ralley.get_last_shot(),
                              depth=new_ralley.get_len_ralley(),
                              n_visits=0,
                              n_wins=0)
        
        # Here we add the edge between the new node and the active node
        # and also set the new node to active
        if (ralley.Ralley.get_len_ralley(new_ralley) == 1):
            # If the Node is the first shot in a ralley, it's added to 
            # State 0
            new_tree.add_new_edge(0, new_tree.get_node_index(), 0, 0, 0)
            new_tree.set_active_node(new_tree.get_node_index())
            node_start = new_tree.get_active_node()
        else:
            # If the ralley is ongoing, here the Edges are added
            # print("Ralley length is not 1")
            node_start = new_tree.get_active_node()
            new_tree.add_new_edge(node_start, 
                                  new_tree.get_node_index(), 
                                  0, 
                                  0, 
                                  0)
            new_tree.set_active_node(new_tree.get_node_index())
    #print("Active Node: " + str(new_tree.get_active_node()))
    new_tree.add_node_visit(new_tree.get_active_node())
    # If the added shot was a terminal shot, the initial state is set to
    # active
    if (new_ralley.get_last_char_of_last_shot()
        in const.ShotEncodings.TERMINALS):

        # The visited Nodes List is used to update the visit counts on 
        # each edge, that has been visited durcing the ralley
        #print("List of visited Nodes: " + str(new_tree.get_visited_nodes()))
        
        new_tree.update_edge_visit_counts()
        new_tree.update_node_visit_counts()
        new_tree.update_node_wins(new_ralley.get_last_char_of_last_shot(), 
                                  colour)
        new_tree.update_edge_wins(new_ralley.get_last_char_of_last_shot(), 
                                  colour)
        new_tree.update_uct_value()
        


        #new_tree.update_uct_value()
        # The visited node list is being deleted
        new_tree.clear_visited_nodes()

        # Also the initial state is set to active
        new_tree.set_active_node(0)
        node_start = 0

    #print("Visited_nodes: " + str(new_tree.get_visited_nodes()))
    #ralley_tree.Ralley_Tree.show_tree(new_tree)

def main_loop():
    run = True
    clock = pygame.time.Clock()
    # Set MANUAL to true to be able to play with arrow keys
    MANUAL = False
    # Set to false to safe time and not display the transition animation
    # of the ball
    TRANSITION_ANIMATION = True

    bottom_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, 
                               HEIGHT - PLAYER_HEIGHT - 10, 
                               PLAYER_WIDTH, 
                               PLAYER_HEIGHT,
                               const.Colours.LIGHT_BLUE)
    top_player = PlayerRect(WIDTH//2 - PLAYER_WIDTH//2, 10, 
                            PLAYER_WIDTH, 
                            PLAYER_HEIGHT,
                            const.Colours.LIGHT_GREEN)
    new_ball = ball.Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    new_ralley = ralley.Ralley()
    new_log = log.Log()
    new_tree = ralley_tree.Ralley_Tree()
    
    # The options are displayed to see what kind of game was started
    print("Simulation: " + str(const.MenuVariables.simulation))
    print("No of Games: " + str(const.MenuVariables.simu_matches))
    print("Top Bot: " + str(const.MenuVariables.top_bot))
    print("Bottom Bot: " + str(const.MenuVariables.bottom_bot))
    print("Animation time: " + str(const.MenuVariables.animation_time))
    print("Sets to play: " + str(const.MenuVariables.sets_to_play))

    # Different classes for Top Bot are initialized depending on the 
    # choice in the main menu
    if const.MenuVariables.top_bot == 1:
        top_bot = bot.Bot("Random")
    elif const.MenuVariables.top_bot == 2:
        top_bot = stat_bot_djokovic.Stat_Bot_Djokovic("Djokovic")
    elif const.MenuVariables.top_bot == 3:
        top_bot = (simpler_stat_bot_djoko.
                   Simple_Stat_Bot_Djokovic("Simple_Djoko"))
    else: top_bot = bot.Bot("Random")

    # Different classes for Bottom Bot are initialized depending on the 
    # choice in the main menu
    if const.MenuVariables.bottom_bot == 1:
        bottom_bot = bot.Bot("Random")
    elif const.MenuVariables.bottom_bot == 2:
        bottom_bot = stat_bot_djokovic.Stat_Bot_Djokovic("Djokovic")
    elif const.MenuVariables.bottom_bot == 3:
        bottom_bot = (simpler_stat_bot_djoko.
                      Simple_Stat_Bot_Djokovic("Simple_Djoko"))
    elif const.MenuVariables.bottom_bot == 4:
        bottom_bot = mcts_agent.MCTS_Agent("MCTS Agent")
    else: bottom_bot = bot.Bot("Random")

    next_button = button.Button(0.05*WIDTH, 0.05*HEIGHT, WIDTH*0.2, 
                                HEIGHT*0.05, "NEXT", const.Colours.BLACK)
    score_text_field = button.Button(0.05*WIDTH, 0.15*HEIGHT, WIDTH*0.2, 
                                     HEIGHT*0.05, "0-0", const.Colours.BLACK)
    new_score = scoring.Scoring(0, 0, 0, 0, 0, 0, "bottom_player")

    # the bottom player always starts the first game in the first set of
    # the match (1 for Bottom player, 2 for top player)
    new_score.set_serving_player(1) 
    new_ball.reset_ball(new_score.get_serving_player(), 
                        new_ralley.get_shot_count())

    set_counting_for_tree = 0
    match_count_for_tree = 0

    while run:
        draw(WIN, [bottom_player, top_player], 
             new_ball, [next_button, score_text_field])
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
            if (event.type == pygame.MOUSEBUTTONDOWN 
                and next_button.check_button_collision(mouse_pos) 
                and const.MenuVariables.simulation == False):
                # Take turns in getting shots from the bot and from the 
                # users If mouse button is pressed on the Next Button a 
                # turn is taken

                # This if elif statement looks at which player is 
                # serving in the game and sets the turn accordingly 
                # before each new ralley, so always the correct player 
                # starts the ralley
                # ToDo: set turn for service for tiebreak
                if (new_score.get_serving_player() == 1 
                    and new_ralley.get_shot_count() == 0):
                    top_bot.set_turn(False)
                elif (new_score.get_serving_player() == 2 
                      and new_ralley.get_shot_count() == 0):
                    top_bot.set_turn(True)
                #print(new_score.get_serving_player())
                #print(new_ralley.get_shot_count())
                # If its not the bots turn, take the ball position as 
                # shot by the user/by the bottom bot
                if top_bot.get_turn() == False:
                    # This is the manual shot encoding, taking the ball 
                    # position set by arrow keys into account
                    if MANUAL:
                        encode_shot_selection(new_ball, new_ralley)
                    else:
                        # The bottom bot adds a shot here
                        bottom_bot.add_shot(new_ralley, new_score, new_tree)
                        tree_update(new_ralley, new_tree, "blue")
                        
                        move_ball_to_pos(new_ball, new_ralley, WIN, 
                                         TRANSITION_ANIMATION, 
                                         "bottom", new_score)
                    top_bot.set_turn(True)

                    # If its the bots turn, call function that gets the 
                    # shot from the bot
                elif top_bot.get_turn() == True:
                    top_bot.add_shot(new_ralley, new_score, new_tree)

                    tree_update(new_ralley, new_tree, "green")

                    # Ball Movement is an animated transition
                    move_ball_to_pos(new_ball, new_ralley, WIN, 
                                     TRANSITION_ANIMATION, "top", new_score)
                    top_bot.set_turn(False)
                    
                # Here the score is updated, depending on the ralley and
                # the shot count and the turn
                new_ralley.score_update(new_score, new_ball)
                if (new_score.get_set_count() != set_counting_for_tree):
                    set_counting_for_tree = new_score.get_set_count()
                    ralley_tree.Ralley_Tree.show_tree(new_tree)

                if const.Changing.ralley_terminated:
                    score_text_field.update_text(str(new_score.get_score()), 
                                             WIN, const.Colours.BLACK)
                    
                    #ralley_tree.Ralley_Tree.show_tree(new_tree)

                    if const.MenuVariables.logging == True:
                        new_log.add_score_to_df(new_score.get_points_A(),
                                                new_score.get_points_B(),
                                                new_score.get_games_A(),
                                                new_score.get_games_B(),
                                                new_score.get_sets_A(),
                                                new_score.get_sets_B(),
                                                new_score.get_serving_player(),
                                                new_ralley.get_last_ralley())
                    const.Changing.ralley_terminated = False
                
        
        if const.MenuVariables.simulation == True:
            while new_score.matches_played < const.MenuVariables.simu_matches:
                
                if (new_score.get_serving_player() == 1 
                    and new_ralley.get_shot_count() == 0):
                    top_bot.set_turn(False)
                elif (new_score.get_serving_player() == 2 
                      and new_ralley.get_shot_count() == 0):
                    top_bot.set_turn(True)
                # If its not the bots turn, take the ball position as 
                # shot by the user/by the bottom player
                if top_bot.get_turn() == False:
                    # This is the manual shot encoding, taking the ball 
                    # position set by arrow keys into account
                    if MANUAL:
                        encode_shot_selection(new_ball, new_ralley)
                    else:
                        # The bottom bot adds a shot here
                        bottom_bot.add_shot(new_ralley, new_score, new_tree)
                        tree_update(new_ralley, new_tree, "blue")

                        move_ball_to_pos(new_ball, new_ralley, WIN, 
                                         TRANSITION_ANIMATION, "bottom", 
                                         new_score)
                    top_bot.set_turn(True)

                    # If its the bots turn, call function that gets the 
                    # shot from the bot
                elif top_bot.get_turn() == True:
                    top_bot.add_shot(new_ralley, new_score, new_tree)
                    tree_update(new_ralley, new_tree, "green")

                    # Ball Movement is an animated transition
                    move_ball_to_pos(new_ball, new_ralley, WIN, 
                                     TRANSITION_ANIMATION, "top", new_score)
                    top_bot.set_turn(False)
                    
                # Here the score is updated, depending on the ralley and 
                # the shot count and the turn
                new_ralley.score_update(new_score, new_ball)
                
                if (new_score.get_match_count() != match_count_for_tree):
                    match_count_for_tree = new_score.get_match_count()
                    ralley_tree.Ralley_Tree.show_tree(new_tree)


                if const.Changing.ralley_terminated:
                    score_text_field.update_text(str(new_score.get_score()), 
                                             WIN, const.Colours.BLACK)
                    if const.MenuVariables.logging == True:
                        new_log.add_score_to_df(new_score.get_points_A(),
                                                new_score.get_points_B(),
                                                new_score.get_games_A(),
                                                new_score.get_games_B(),
                                                new_score.get_sets_A(),
                                                new_score.get_sets_B(),
                                                new_score.get_serving_player(),
                                                new_ralley.get_last_ralley())
                    const.Changing.ralley_terminated = False

                draw(WIN, [bottom_player, top_player], new_ball, 
                     [next_button, score_text_field])
    pygame.QUIT

if __name__ == "__main__":
        main_loop()