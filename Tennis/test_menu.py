import pygame_menu
from pygame_menu.examples import create_example_window

import main_loop
import constants as const

SURFACE = create_example_window('PyTennis', 
                                (const.Dims.WIDTH, 
                                 const.Dims.HEIGHT))

# The menu is created with a theme and caption 
# as well as the dimensions
menu = pygame_menu.Menu(
    height=const.Dims.HEIGHT,
    theme=pygame_menu.themes.THEME_GREEN,
    title='Main Menu',
    width=const.Dims.WIDTH
)

def start_the_game():
    # This function calls the main Game loop
    main_loop.main_loop()

def set_animation(selected: tuple, value: any):
    # Animation Time is set here. If its going 
    # fast medium or slow speed
    if value == 1:
        const.MenuVariables.animation_time = 0.00
    elif value == 2:
        const.MenuVariables.animation_time = 0.025
    elif value == 3:
        const.MenuVariables.animation_time = 0.05
        
def set_sets_to_play(selected:tuple, value: any):
    # Decides if the match is best of five or best of 3
    if value == 1:
        const.MenuVariables.sets_to_play = 3
    elif value == 2:
        const.MenuVariables.sets_to_play = 5

def set_top_player(selected:tuple, value: any):
    # Top Players strategy is set
    if value == 1:
        const.MenuVariables.top_bot = 1
    elif value == 2:
        const.MenuVariables.top_bot = 2

def set_bottom_player(selected:tuple, value: any):
    # Bottom Players strategy is set 
    if value == 1:
        const.MenuVariables.bottom_bot = 1
    elif value == 2:
        const.MenuVariables.bottom_bot = 2

def set_simu_game_no(value: any):
    x = int(value)
    const.MenuVariables.simu_matches = x

def simulation_bool(selected:tuple, value: any):
    if value == 1:
        const.MenuVariables.simulation = True
    else: const.MenuVariables.simulation = False

def set_color_scheme(selected:tuple, value: any):
    if value == 1:
        const.MenuVariables.color_scheme = 1
    elif value == 2:
        const.MenuVariables.color_scheme = 2
    elif value == 3:
        const.MenuVariables.color_scheme = 3
    elif value == 4:
        const.MenuVariables.color_scheme = 4

def set_logging(selected: tuple, value: any):
    if value == 1:
        const.MenuVariables.logging = False
    elif value == 2:
        const.MenuVariables.logging = True

# Menu options are being added
menu.add.selector('Mode: ', 
                  [('Simulation', 1), ('Manual', 2)], 
                  default=0, 
                  onchange=simulation_bool)
menu.add.range_slider('Number of Matches: ', 
                      default=1, range_values=[1,10], 
                      increment=int(1), 
                      range_text_value_enabled = False, 
                      slider_text_value_enabled=True, 
                      onchange=set_simu_game_no)
menu.add.selector('Top Player: ', 
                  [('Random', 1), ('Djokovic', 2)], 
                  default=0, 
                  onchange=set_top_player)
menu.add.selector('Bottom Player: ', 
                  [('Random', 1), ('Djokovic', 2)], 
                  default=0, 
                  onchange=set_bottom_player)
menu.add.selector('Animation time: ', 
                  [('Fast', 1), ('Medium', 2), ('Slow', 3)], 
                  default=0, 
                  onchange=set_animation)
menu.add.selector('Best of: ', 
                  [('3', 1), ('5', 2)], 
                  default=0, 
                  onchange=set_sets_to_play)
menu.add.selector('Tournament: ', 
                  [('US Open', 1), ('Roland Garros', 2), 
                   ('Australien Open', 3), ('Wimbledon', 4)], 
                  default=0, 
                  onchange=set_color_scheme)
menu.add.selector('Export Data: ',
                  [('Off', 1), ('On', 2)],
                  default=0,
                  onchange=set_logging)
menu.add.button('Play', 
                start_the_game)
menu.add.button('Quit', 
                pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(SURFACE)