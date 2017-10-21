#Volleyball simulation
import pygame as pg, math
import functions

#screen size
screen_size=(800,600)

#initializes object for framerate
clock=pg.time.Clock()

#making screen
screen=pg.display.set_mode(screen_size)
pg.display.set_caption('Volleyball')

#initial position of players
x_red=50
y_red=200
x_blue=600
y_blue=450
x_blue_last=600
y_blue_last=450

#position of ball
x=600
y=200
xlast=600
ylast=200




