#Volleyball simulation
import pygame as pg, math
import functions as fn

pg.init()

#screen size
screen_size=(800,600)

#loads and transforms images
fn.load_images()
fn.transform_images()

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

flag=0 #for normal game run

#initial movement
angle=90
lr=0
ud=-1

#Direction map
#       +1
#       / \ 
# -1 <---0---> +1
#       \ / 
#       -1

i=True
while i:
    
    if flag==0: #normal game
        x,y=fn.get_ballpos(angle,lr,ud)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            i=False

        if event.type==pg.KEYDOWN:
            if event.key==pg.K_RIGHT:
                x_blue,lr=fn.get_playerbpos(x,y,x_blue,y_blue,lr)
            if event.key==pg.K_LEFT:
                x_blue,lr=fn.get_playerbpos(x,y,x_blue,y_blue,lr)
        
            




