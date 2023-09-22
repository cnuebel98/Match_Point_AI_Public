class Dims:
    '''This class stores the dimensions of the GUI and the elements in 
    the GUI'''
    # Window size
    WIDTH = 1200
    HEIGHT = 720

    # Size of elements
    BALL_RADIUS = 7
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 40

    # Some timing related stuff
    FPS = 60
    BALL_VELOCITY = 3

    # Court dimensions
    COURT_HEIGHT = int(0.8*HEIGHT)
    COURT_WIDTH = int(0.4615*COURT_HEIGHT)
    LINE_WIDTH = 6
    SINGLES_LINES_WIDTH = int(0.75*COURT_WIDTH)
    TLINE_HEIGHT = int(0.5385*COURT_HEIGHT)
    NET_WIDTH = int(1.2*COURT_WIDTH)

class Colors:
    '''This class stores the colors as RGB Values'''
    # Some Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 136, 0)
    DARK_GREEN = (0, 80, 0)
    BLUE = (0, 164, 255)
    YELLOW = (255, 255, 0)
    GREY = (47, 79, 79)
    
    # French Open Color Scheme:
    CLAY_COURT_COLOR = (194, 69, 45)
    
    # Wimbledon Grass Color Scheme
    WIMBLEDON_GREEN = (0, 123, 34)

    # US Open Color Scheme:
    US_OPEN_GREEN = (108, 147, 92)
    US_OPEN_BLUE = (60, 99, 142)

    # Australien Open Color Scheme:
    AUSOPEN_COURT_BLUE = (55, 125, 184)
    AUSOPEN_COURT_LIGHTBLUE = (30, 143, 213)
    AUSOPEN_LINECOLOR = (232, 247, 255)

class ShotEncodings:
    '''This class stores all the Shot encodings in their respective 
    categories'''
    WINNER = "*"
    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    SERVE_DIRECTION = ["4", "5", "6"]
    EVERY_SHOT_TYPE = ["f", "b", "r", "s", "v", "z", "o", "p", "y", "l",
                        "m", "h", "i", "j", "k", "t", "u"]
    RETURN_SHOT_TYPES = ["f", "b", "r", "s", "y", "l", "m", "h", "i", 
                         "t", "u"]
    RETURN_DEPTH = ["7", "8", "9"]
    DIRECTIONS = ["1", "2", "3"]
    EXTRA_STUFF = ["+", ";", "^", "S", "R", "C", "!", "0", "-", "=", 
                   "P", "Q", "c", "q", "e", "N"]
    SECOND_SERVE = [","]

class MenuVariables:
    '''The Options from the menu are initialized here and set when the 
    game is started'''
    sets_to_play = 3
    animation = True
    top_bot = 1
    bottom_bot = 1
    animation_time = 0.00
    simu_matches = 1
    simulation = True
    color_scheme = 1
    logging = False

class Changing:
    ralley_terminated = False