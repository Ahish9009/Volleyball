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

tracker_Bx=[0,0,0,0,0]
tracker_Rx=[0,0,0,0,0]
tracker_x=[0,0,0,0,0]
tracker_y=[0,0,0,0,0]

jumpblue=False

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
        
        if jumpblue:
            y_blue,jumpblue,jumpbcount=fn.bluejump(y_blue,jumpblue,jumpbcount)
            
        #ai
        x_red=fn.get_AI(side,lr,x,x_red)
        

        #get velocity of blue player
        bluevel=fn.get_bluevel(tracker_Bx)

        #get velocity of red player
        redvel=fn.get_redvel(tracker_Rx)
    
        #checks if the ball touches the edges of the screen
        #to check if the ball is in contact with the top
        contact_top=fn.checkcontact_top(y)
        #to check if the ball is in contact with the sides
        contact_sides=fn.checkcontact_sides(x)

        #checks if the ball touches the blue player
        #to check if ball is in contact with the side of the player
        contact_BLUEe,pos_Be=fn.checkcontact_BLUEedge(x,y,x_blue,y_blue)
        #to check if the ball is in contact with the top of the player
        contact_BLUEt=fn.checkcontact_BLUEtop(x,y,x_blue,y_blue,tracker_y)
        #to check if the ball is in contact with the side of the player
        contact_BLUEs,pos_s=fn.checkcontact_BLUEside(x,y,x_blue,y_blue,tracker_x,lr)

        #checks if the ball touches the rod
        #to check if the ball is in contact with the side of the rod
        contact_RODs=fn.checkcontact_RODside(x,y,tracker_x,lr)
        #to check if the ball is in contact with the edge of the rod
        contact_RODe,toinvert=fn.checkcontact_RODedge(x,y,tracker_y,lr,ud)
        #to check if the ball is in contact with the top of the rod
        contact_RODt=fn.checkcontact_RODtop(x,y,tracker_y)

        #checks if the ball touches the red player
        #to check if the ball is in contact with the edge of the red player
        contact_REDe,pos_Re=fn.checkcontact_REDedge(x,y,x_red,y_red)
        #to check if the ball is in contact with the top of the red player
        contact_REDt=fn.checkcontact_REDtop(x,y,x_red,y_red,tracker_y)

        angle,lr,ud,y=fn.get_details_s1(y,angle,lr,ud,pos_Be,pos_Re,pos_s,toinvert,bluevel,redvel,contact_top,contact_sides,contact_RODs,contact_RODe,contact_RODt,contact_BLUEe,contact_BLUEt,contact_BLUEs,contact_REDe,contact_REDt)

        if angle<25:
            angle=25

        if angle>155:
            angle=155
        
        x,y,angle,lr,ud=fn.get_ballpos(x,y,angle,lr,ud)

    for event in pg.event.get():
        if event.type==pg.QUIT: 
            i=False

        if event.type==pg.KEYDOWN:
            
            if event.key==pg.K_RIGHT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'r')
            elif event.key==pg.K_LEFT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'l')
            if event.key==pg.K_SPACE:
                if not jumpblue:
                    jumpblue=True
                    jumpbcount=0

    if y+72>600:
        y=100

    screen.blit(bg, (0,0))
    screen.blit(rod, (393,300))
    screen.blit(playerr, (x_red,y_red))
    screen.blit(playerb, (x_blue,y_blue))
    screen.blit(volleyball, (x,y))

    lr=fn.lr_checker(tracker_x,x) #as lr can go wrong

    tracker_Bx=fn.tracker_BLUEx(tracker_Bx,x_blue)
    tracker_Rx=fn.tracker_REDx(tracker_Rx,x_red)
    tracker_x=fn.tracker_ballx(tracker_x,x)
    tracker_y=fn.tracker_bally(tracker_y,y)
    side=fn.ballside(x,tracker_x,lr,side)

    pg.display.update()
    clock.tick(100) #decides maximum fps

pg.quit()
