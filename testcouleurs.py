def init_bonus():
    multipliers = [
    4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4,
    0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3, 0,
    0, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0,
    1, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0,
    0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0,
    0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
    4, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 4,
    0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
    0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0,
    1, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1,
    0, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0,
    0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3, 0,
    4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4
    ]
    return multipliers

init_bonus()
 
current_board = init_bonus()[:]
import pygame
from pygame.locals import *

pygame.init()

window_resolution = (640, 480)
pygame.display.set_mode()

window_surface = pygame.display.set_mode(window_resolution)

WIDTH, HEIGHT = 800,800
ROWS, COLS = 15, 15
SQUARE_SIZE = WIDTH//COLS
RED = (255,0,0)
GREEN = (0,255,0)
GOLDENROD = (218,165,32)
CRIMSON = (220,20,60)
STEELBLUE = (70,130,160)
LIGHTBLUE = (173,216,230)
BLACK = (0,0,0)
WIDTH, HEIGHT = 800,800
board = init_bonus()
rect_form = pygame.Rect(30, 30, 60, 60)

def affiche_plateau(board):
            if board == 4:
                pygame.draw.rect(window_surface, CRIMSON, rect_form)
                
                #print 'MT',
            elif board == 3:
                pygame.draw.rect(window_surface, GOLDENROD, rect_form)
                
                #print 'WD',
            elif board == 2:
                pygame.draw.rect(window_surface, STEELBLUE, rect_form)
                
                #print 'LT',
            elif board == 1:
                pygame.draw.rect(window_surface, LIGHTBLUE, rect_form)
                
                #print 'LD',
            elif board  == 0:
                pygame.draw.rect(window_surface, GREEN, rect_form)
affiche_plateau(init_bonus())

pygame.display.flip()
