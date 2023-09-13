import pygame_menu
from pygame_menu.examples import create_example_window

import main_loop
import constants as const

SURFACE = create_example_window('PyTennis', (const.Dims.WIDTH, const.Dims.HEIGHT))
animations = True
sets_to_play = 3

menu = pygame_menu.Menu(
    height=const.Dims.HEIGHT,
    theme=pygame_menu.themes.THEME_GREEN,
    title='Main Menu',
    width=const.Dims.WIDTH
)

def start_the_game():
    main_loop.main_loop()

def set_animation(selected: tuple, value: any):
    if value == 1:
        animations = True
    elif value == 2:
        animations = False

def get_animation():
    return animations
        
def set_sets_to_play(selected:tuple, value: any):
    if value == 1:
        sets_to_play = 3
    elif value == 2:
        sets_to_play = 5

def get_sets_to_play():
    return sets_to_play

menu.add.selector('Animations: ', [('On', 1), ('Off', 2)], onchange=set_animation)
menu.add.selector('Best of ', [('3', 1), ('5', 2)], onchange=set_sets_to_play)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(SURFACE)