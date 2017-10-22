
#Volleyball simulation
import pygame as pg, math
import functions as fn

pg.init()

#screen size
screen_size=(800,600)

#loads and transforms images
bg,rod,playerr,playerb,volleyball=fn.load_images()

#initializes object for framerate
clock=pg.time.Clock()

#making screen
screen=pg.display.set_mode(screen_size)
pg.display.set_caption('Volleyball')

#initial position of players
x_red=50
y_red=450
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
side=1


tracker_x=[0,0,0,0,0]

#to repeat
pg.key.set_repeat(10, 5)

#Direction map
#       +1 
#       / \ 
# -1 <---0---> +1
#       \ / 
#       -1

i=True
while i:

    if flag==0: #normal game
        x,y,angle,lr,ud=fn.get_ballpos(x,y,angle,lr,ud)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            i=False

        if event.type==pg.KEYDOWN:
            if event.key==pg.K_RIGHT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'r')
            if event.key==pg.K_LEFT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'l')

    screen.blit(bg, (0,0))
    screen.blit(rod, (393,300))
    screen.blit(playerr, (x_red,y_red))
    screen.blit(playerb, (x_blue,y_blue))
    screen.blit(volleyball, (x,y))

    tracker_x=fn.tracker_ballx(tracker_x,x)
    side=fn.ballside(x,tracker_x,lr,side)

    pg.display.update()

pg.quit()



