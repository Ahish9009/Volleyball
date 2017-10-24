import pygame as pg,math

#(x-36)^2 +(y-36)^2 = 36^2
y1=0
ball_coordinates=[]
while y1<=72:
    x1=36-math.sqrt(36**2 - (y1-36)**2)
    x2=36+math.sqrt(36**2 - (y1-36)**2)
    ball_coordinates+=[[int(x1),int(x2)]]
    y1+=1


#to load images
def load_images():
    bg=pg.image.load('pictures/bg.png')
    rod=pg.image.load('pictures/rod.png')
    playerr=pg.image.load('pictures/player red.jpg')
    playerb=pg.image.load('pictures/player blue.jpg')
    volleyball=pg.image.load('pictures/volleyball.png')
    #transforms images
    bg=pg.transform.scale(bg, (800,600))
    rod=pg.transform.scale(rod, (14,300))
    playerr=pg.transform.scale(playerr, (85,150))
    playerb=pg.transform.scale(playerb, (85,150))
    volleyball=pg.transform.scale(volleyball, (72,72)) #r=36

    return bg,rod,playerr,playerb,volleyball

#to invert directions
def invert(variable):
    variable*=(-1)
    return variable

def tracker_BLUEx(tracker_Bx,x_blue): #stores the last 5 positions of the ball with the latest being first
    new=tracker_Bx
    for i in range(4,0,-1):
        new[i]=new[i-1]
    new[0]=x_blue
    return new #returns the new ball x tracker

def tracker_ballx(tracker_x,x): #stores the last 5 positions of the ball with the latest being first
    new=tracker_x
    for i in range(4,0,-1):
        new[i]=new[i-1]
    new[0]=x
    return new #returns the new ball x tracker

def tracker_bally(tracker_y,y): #stores the last 5 positions of the ball with the latest being first
    new=tracker_y
    for i in range(4,0,-1):
        new[i]=new[i-1]
    new[0]=y
    return new #returns the new ball y tracker

def get_bluevel(tracker_Bx): #Gets direction in which the blue player is moving
    if tracker_Bx[0]==tracker_Bx[1]:
        bluevel=0
        return bluevel
    if tracker_Bx[0]>tracker_Bx[1]:
        bluevel=1
        return bluevel
    if tracker_Bx[0]<tracker_Bx[1]:
        bluevel=-1
        return bluevel

def ballside(x,tracker_x,lr,side): #mainly for player position hence middle case not included
    if x<400 and tracker_x[1]<400:
        side=-1
        
    if x==400:
        if tracker_x[1]<400:
            side=1 
        if tracker_x[1]>400:
            side=-1 
            
    if x<400 and tracker_x[1]>400:
        side=1

    return side

def bluejump(y_blue,jumpblue,jumpbcount):
    if jumpbcount<100:
        y_blue-=2
    elif jumpbcount>=100 and jumpbcount<150:
        y_blue+=4
    else:
        y_blue=450
        jumpblue=False
    jumpbcount+=1
    return y_blue,jumpblue,jumpbcount

def checkcontact_top(y):
    if y<=0:
        return True

def checkcontact_sides(x):
    if x<=0 or x+72>=800:
        return True

def checkcontact_RODtop(x,y,tracker_y):
    contact=False
    if x+36>=393 and x+36<=407:
        if tracker_y[1]+72<300 and y+72>=300:
            contact=True
    return contact

def checkcontact_RODside(x,y,tracker_x,lr):
    contact=False
    if y+36>300:
        if x<=407 and tracker_x[3]>407 and lr==-1:
            contact=True
        elif x+72>=393 and tracker_x[3]+72<393 and lr==1:
            contact=True

    return contact

def checkcontact_RODedge(x,y,tracker_y,lr,ud):
    contact=False
    toinvert=False

    if y+72>=300 and y+36<300:

        if x+36<393: #top left edge
            
            overlap=y+72-300
            y1=72-overlap

            for i in range(72,y1,-1):
                if 393>x+ball_coordinates[i][1]:
                    contact=False
                else:
                    contact=True
                    if tracker_y[3]>=300+36:
                        toinvert=1 #inverts only horizontal
                    else:
                        if lr==1:
                            toinvert=2 #inverts vertical and horizontal
                        if lr==-1:
                            if ud==1:
                                toinvert=1
                            if ud==-1:
                                toinvert=3 #inverts only vertical

        if x+36>407: #top right edge
            overlap=y+72-300
            y1=72-overlap

            for i in range(72,y1,-1):
                if 407<x+ball_coordinates[i][0]:
                    contact=False
                else:
                    contact=True
                    if tracker_y[3]>=300+36:
                        toinvert=1 #inverts only horizontal
                    else: 
                        if lr==1:
                            toinvert=3 #inverts only vertical
                        if lr==-1:
                            if ud==1:
                                toinvert=1
                            if ud==-1:
                                toinvert=2 #inverts vertical and horizontal
    return contact,toinvert
    
def checkcontact_BLUEedge(x,y,x_blue,y_blue):
    contact=False
    pos=''
    
    if y+72>=y_blue and y+36<y_blue: #if the lower half of the ball is touching the edge
 
        if x+36<x_blue: #check contact on top left edge

            overlap = y+72-y_blue
            y1=72-overlap

            for i in range(72,y1,-1):
                if x_blue>x+ball_coordinates[i][1]:
                    contact=False
                else:
                    contact=True
                    pos='lt'
                    
        if x+36>x_blue+85: #check contact on right edge of player
            overlap = y+72-y_blue
            y1=72-overlap
            
            for i in range(72,y1,-1):
                
                if x_blue+85<x+ball_coordinates[i][0]:
                    contact=False
                else:
                    contact=True
                    pos='rt'
                    
        return contact,pos

    elif y+72<y_blue:
        return contact, pos
    else:
        return contact, pos
        
def checkcontact_BLUEtop(x,y,x_blue,y_blue,tracker_y):
    contact=False
    if x+36>=x_blue and x+36<=x_blue+85:
        if tracker_y[3]+72<y_blue and y+72>=y_blue:
            contact=True
    return contact

def checkcontact_BLUEside(x,y,x_blue,y_blue,tracker_x,lr):  #if the ball touches the side of the player
    contact=False
    pos=''
    if y+36>=y_blue and y+36<=y_blue+150:
        if lr!=0:
            if tracker_x[1]+72<x_blue and x+72>=x_blue: #hitting the left side
                contact=True
                pos='ls'
            elif tracker_x[1]>x_blue+85 and x<=x_blue+85: #hitting the right side
                contact=True
                pos='rs'
        else:
            if x+72>=x_blue and x+72<x_blue+40: #hitting the left side
                contact=True
                pos='ls'
            elif x<=x_blue+85 and x>x_blue+20: #hitting the right side
                contact=True
                pos='rs'
    return contact,pos
    
def get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,movement):

    if movement=='l':
        change=-1
    else:
        change=1
    
    if side!=1:
        if x_blue==407:
            if change==1:
                x_blue+=change

            return x_blue
        elif x_blue+85==800:
            if change==-1:
                x_blue+=change

            return x_blue
        else:
            x_blue+=change
            return x_blue

    if side==1:
        if y+72<y_blue: #when ball is above the player
            if x_blue==407:
                if change==1:
                    x_blue+=change
    
                return x_blue
            elif x_blue+85==800:
                if change==-1:
                    x_blue+=change

                return x_blue
            else:
                x_blue+=change
                return x_blue

        if y+72>=y_blue and y+36<y_blue: #when part of the ball is below the players top
            contact,pos=checkcontact_BLUEedge(x,y,x_blue,y_blue)

            if contact:
                return x_blue            
            else:
                if x_blue==407:
                    if change==1:
                        x_blue+=change
                    return x_blue
                elif x_blue+85==800:
                    if change==-1:
                        x_blue+=change
                    return x_blue
                else:
                    x_blue+=change
                    return x_blue

        if y+36>=y_blue and y+36<y_blue+150: #when half the ball is below the player

            if lr==0: #if it is going straight down
                if x==407: #If the ball is touching the net
                    if x_blue<=407+72:
                        if change==-1:
                            return x_blue
                        if change==1:
                            x_blue+=change
                            return x_blue
                    if x_blue>407+72:
                        if change==-1:
                            x_blue+=change
                        if change==1:
                            if x_blue+85<=800:
                                x_blue+=change
                        return x_blue
                elif x+72==800:
                    if x_blue>=800-72:
                        if change==1:
                            return x_blue
                        if change==-1:
                            x_blue+=change
                            return x_blue
                    if x_blue<800-72:
                        if change==1:
                            x_blue+=change
                        if change==-1:
                            if x_blue>407:
                                x_blue+=change
                        return x_blue
                else:
                    if x_blue==800-85:
                        if change==1:
                            return x_blue
                        if change==-1:
                            x_blue+=change
                            return x_blue
                    if x_blue==407:
                        if change==1:
                            x_blue+=change
                            return x_blue
                        if change==-1:
                            return x_blue
                        
                    x_blue+=change
                    return x_blue
            else:
                if x_blue==407:
                    if change==1:
                        x_blue+=change
        
                    return x_blue
                elif x_blue+85==800:
                    if change==-1:
                        x_blue+=change

                    return x_blue
                else:
                    x_blue+=change
                    return x_blue           

def get_details_s1(y,angle,lr,ud,pos_e,pos_s,toinvert,bluevel,contact_top,contact_sides,contact_RODs,contact_RODe,contact_RODt,contact_BLUEe,contact_BLUEt,contact_BLUEs): #s1 for side=1

    if contact_top: 
        ud=-1
        angle=180-angle #to reflect the ball

    elif contact_sides:
        lr=invert(lr)
        angle=180-angle

    elif contact_RODs:
        lr=invert(lr)
        angle=180-angle

    elif contact_RODe:
        if toinvert==1:
            lr=invert(lr)
            angle=180-angle
        if toinvert==2:
            lr=invert(lr)
            ud=invert(ud)
        if toinvert==3:
            ud=invert(ud)
            angle=180-angle

    elif contact_RODt:
        ud=invert(ud)
        angle=180-angle

    elif contact_BLUEt: #if the ball is touching the top face of the ball
        
        if bluevel==0:
            y-=2
            angle=180-angle
            ud=invert(ud)

        elif bluevel==1:
            ud=invert(ud)
            if lr==0:
                angle=(angle+180)/2
                lr=1
                y-=2
            elif lr==1:
                angle=180-angle
                angle=(180+angle)/2
                y-=2
            elif lr==-1:
                angle=180-angle
                angle=(90+angle)/2
                y-=2

        elif bluevel==-1:
            ud=invert(ud)
            if lr==0:
                y-=2
                angle=(angle+0)/2
                lr=-1
            elif lr==1:
                y-=2
                angle=180-angle
                angle=(90+angle)/2
            elif lr==-1:
                y-=2
                angle=180-angle
                angle=angle/2
            
    elif contact_BLUEe: #if the ball is touching the corner of the player
            if lr==0:
                if pos_e=='lt':
                    ud=1
                    angle=(0+angle)/2
                    lr=-1
                if pos_e=='rt':
                    ud=1
                    angle=(angle+180)/2
                    lr=1
                
            elif lr==1: #if ball is moving towards the right
                if pos_e=='lt':
                    ud=1
                    lr=invert(lr)
                if pos_e=='rt':
                    angle=180-angle
                    ud=1
            elif lr==-1: #if ball is moving towards the left
                if pos_e=='lt':
                    ud=1
                    angle=180-angle
                if pos_e=='rt':
                    ud=1
                    lr=invert(lr)
            y-=2

    elif contact_BLUEs:
        if lr==0:
            if pos_s=='ls':
                lr=-1
                angle=(180+angle)/2
            elif pos_s=='rs':
                lr=1
                angle=angle/2
        else:
            if pos_s=='ls':
                angle=180-angle
                lr=invert(lr)
            elif pos_s=='rs':
                angle=180-angle
                lr=invert(lr)

    return angle,lr,ud,y

                 
def get_ballpos(x,y,angle,lr,ud):

    if x<0:
        x=1
    if x+72>800:
        x=799-72

    if lr==0:
        if ud==-1:
            y+=2
            return x,y,angle,lr,ud
        if ud==1:
            y-=2
            return x,y,angle,lr,ud
        return x,y,angle,lr,ud

    if lr==1: #moving to the right
        if ud==1: #moving upwards
            #y=mx+c
            #dy/dx=m
            #dx/dy=1/m
            #dx=2/m
            #angle will be more than 90, thus it has to be made acute
            temp=180-angle #makes it acute
            m=math.tan(math.radians(temp)) #finds m (tan theta)
            dx=3/m
            y-=3
            x+=dx
        elif ud==-1: #moving downwards and angle is already acute 
            m=math.tan(math.radians(angle))
            dx=3/m
            y+=3
            x+=dx
   
        return x,y,angle,lr,ud

    if lr==-1:
        if ud==1:
            m=math.tan(math.radians(angle))
            dx=3/m
            y-=3
            x-=dx
        if ud==-1: #angle is obtuse as it is going to the left downwards
            temp=180-angle
            m=math.tan(math.radians(temp))
            dx=3/m
            y+=3
            x-=dx
         
        return x,y,angle,lr,ud
