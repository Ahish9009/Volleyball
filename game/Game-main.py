#Volleyball simulation
#Importing required Libraries
import pygame as pg, math
import functions as fn

pg.init()

#screen size
screen_size=(800,600)

#loads and transforms images
bg,rod,playerr,playerb,volleyball,overlay1,overlay2=fn.load_images()

#loads fonts
TNR1=pg.font.SysFont("Times New Roman", 50)
TNR2=pg.font.SysFont("Times New Roman", 30)

PETC=TNR1.render('Press enter to exit...',1,(0,0,0))
paused=TNR1.render('PAUSED',1,(0,0,0))
welcome=TNR1.render('WELCOME!',1,(0,0,0))
choice=TNR2.render('Select the difficult level:',1,(0,0,0))
choice1=TNR2.render('Easy - Press 1',1,(0,0,0))
choice2=TNR2.render('Medium - Press 2',1,(0,0,0))
choice3=TNR2.render('Difficult - Press 3',1,(0,0,0))

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

flag=-1 #for welcome screen

#initial movement
angle=90
lr=0
ud=-1
side=1

tracker_Bx=[0,0,0,0,0]
tracker_Rx=[0,0,0,0,0]
tracker_x=[0,0,0,0,0]
tracker_y=[0,0,0,0,0]

#Initialization of the scores of Red and Blue
red_score=0
blue_score=0
red_touch=0
blue_touch=0

delay_b=False
delay_r=False

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
    #initial check if a player has won
    scorer=TNR1.render(str(red_score)+' - '+str(blue_score),1,(0,0,0))
    bluetouch=TNR2.render(str(3-blue_touch),1,(50,50,50))
    redtouch=TNR2.render(str(3-red_touch),1,(50,50,50))
    if red_score==15:
        redwon=TNR1.render('Sorry, the computer has won...',1,(0,0,0))
        flag=1
    elif blue_score==15:
        flag=2
        bluewon=TNR1.render('Congrats! You beat the computer!!',1,(0,0,0))

    if flag==-1:
        screen.blit(bg, (0,0))
        screen.blit(welcome, (300,275))
        screen.blit(choice, (250,350))
        screen.blit(choice1, (250,380))
        screen.blit(choice2, (250,410))
        screen.blit(choice3, (250,440))
        
    if flag==3: #pauses
        screen.blit(bg, (0,0))
        screen.blit(paused, (300,275))

    if flag==1: #if red wins
        screen.blit(bg, (0,0))
        screen.blit(redwon, (50,250))
        screen.blit(scorer,(300,330))
        screen.blit(PETC, (400,550))

    if flag==2: #if blue wins
        screen.blit(bg, (0,0))
        screen.blit(bluewon, (50,250))
        screen.blit(scorer,(300,330))
        screen.blit(PETC, (400,550))
    
    if flag==0: #normal game
        if delay_b: #delay to get contact as True after hitting the player once
            if delay_bcount==50:
                delay_b=False
            delay_bcount+=1

        if delay_r: #delay to get contact as True after hitting the player once
            if delay_rcount==50:
                delay_r=False
            delay_rcount+=1
        
        if jumpblue: #condition for the blue player to jump and call of the blue jump function
            y_blue,jumpblue,jumpbcount=fn.bluejump(y_blue,jumpblue,jumpbcount)
            
        #ai
        x_red=fn.get_AI(side,lr,x,y,x_red,speed)
        
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
        if not delay_b:
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
        if not delay_r:
            #to check if the ball is in contact with the edge of the red player
            contact_REDe,pos_Re=fn.checkcontact_REDedge(x,y,x_red,y_red)
            #to check if the ball is in contact with the top of the red player
            contact_REDt=fn.checkcontact_REDtop(x,y,x_red,y_red,tracker_y)
        #to check if the ball is in contact with the side of the red player
        contact_REDs,pos_Rs=fn.checkcontact_REDside(x,y,x_red,y_red,tracker_x,lr)

        angle,lr,ud,y=fn.get_details_s1(y,y_blue,angle,lr,ud,pos_Be,pos_Re,pos_s,pos_Rs,toinvert,bluevel,redvel,contact_top,contact_sides,contact_RODs,contact_RODe,contact_RODt,contact_BLUEe,contact_BLUEt,contact_BLUEs,contact_REDe,contact_REDt,contact_REDs)
        #Checks the angles
        angle,lr,ud,x,y=fn.get_details_s1(x,y,x_red,x_blue,y_blue,angle,lr,ud,pos_Be,pos_Re,pos_s,pos_Rs,toinvert,bluevel,redvel,contact_top,contact_sides,contact_RODs,contact_RODe,contact_RODt,contact_BLUEe,contact_BLUEt,contact_BLUEs,contact_REDe,contact_REDt,contact_REDs)

        if angle<25:
            angle=25

        if angle>155:
            angle=155
        
        x,y,angle,lr,ud=fn.get_ballpos(x,y,angle,lr,ud)

        if contact_BLUEe or contact_BLUEt:  #to check if the call is in contact with the red player
            delay_b=True
            contact_BLUEe,contact_BLUEt=False,False
            delay_bcount=0
            blue_touch+=1
            red_touch=0

        if contact_REDe or contact_REDt:  #to check if the ball is in contact with the red player
            delay_r=True
            contact_REDe,contact_REDt=False,False
            delay_rcount=0
            red_touch+=1
            blue_touch=0

        if y+72>600:
            if side==1:
                screen.blit(overlay1, (0,0))
            if side==-1:
                screen.blit(overlay2, (0,0))
            pg.display.update()
            pg.time.wait(1000)
            if side==1:
                red_score+=1
                x=200
            if side==-1:
                blue_score+=1
                x=600
            y=100
            lr,ud=0,-1
            angle=90
            red_touch,blue_touch=0,0
            
        if blue_touch==4:  # if the blue player has touched the ball 4 times increases the score of red player 
            screen.blit(overlay1, (0,0))
            pg.display.update()
            pg.time.wait(1000)
            red_score+=1
            x=200
            y=100
            lr,ud=0,-1
            angle=90
            blue_touch,blue_touch=0,0
        if red_touch==4:# if the red player has touched the ball 4 times increases the score of blue player 
            screen.blit(overlay2, (0,0))
            pg.display.update()
            pg.time.wait(1000)
            blue_score+=1
            x=600
            y=100
            lr,ud=0,-1
            angle=90
            red_touch,blue_touch=0,0
            
        screen.blit(bg, (0,0))
        screen.blit(rod, (393,300))
        screen.blit(playerr, (x_red,y_red))
        screen.blit(playerb, (x_blue,y_blue))
        screen.blit(scorer, (350,0))
        screen.blit(bluetouch, (770,5))
        screen.blit(redtouch, (10,5))
        screen.blit(volleyball, (x,y))

        lr=fn.lr_checker(tracker_x,x) #as lr can go wrong

        tracker_Bx=fn.tracker_BLUEx(tracker_Bx,x_blue)
        tracker_Rx=fn.tracker_REDx(tracker_Rx,x_red)
        tracker_x=fn.tracker_ballx(tracker_x,x)
        tracker_y=fn.tracker_bally(tracker_y,y)
        side=fn.ballside(x,tracker_x,lr,side)

    for event in pg.event.get():
        if event.type==pg.QUIT: 
            i=False

        if event.type==pg.KEYDOWN:

            if event.key==pg.K_1:
                if flag==-1:
                    speed=1
                    flag=0
            if event.key==pg.K_2:
                if flag==-1:
                    speed=2
                    flag=0
            if event.key==pg.K_3:
                if flag==-1:
                    speed=3
                    flag=0
            if event.key==pg.K_RIGHT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'r')
            elif event.key==pg.K_LEFT:
                x_blue=fn.get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,'l')
            if event.key==pg.K_SPACE:
                if not jumpblue:
                    jumpblue=True
                    jumpbcount=0
            if event.key==pg.K_RETURN:
                if flag==1 or flag==2:
                    i=False
            if event.key==pg.K_p:
                
                if flag==3:
                    flag=flag_o
                elif flag!=3:
                    flag_o=flag #sets original flag where it should come back to
                    flag=3
                           
    pg.display.update()
    clock.tick(100) #decides maximum fps

pg.quit() #to quit the game 
