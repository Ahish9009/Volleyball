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

#to invert direction horizontally
def invert_lr(lr):
    lr*=(-1)
    return lr

#to invert direction vertially
def invert_ud(ud):
    ud*=(-1)
    return ud

def tracker_ballx(tracker_x,x): #stores the last 5 positions of the blue player with the latest being first
    new=tracker_x
    for i in range(4,0,-1):
        new[i]=new[i-1]
    new[0]=x
    return new #returns the new ball x tracker

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

def checkcontact(x,y,x_blue,y_blue):
    contact=False
    if x<x_blue: #check contact on top left edge

        overlap = y+72-y_blue
        y1=72-overlap

        for i in range(72,y1,-1):
            if x_b>x+ball_coordinates[i][1]:
                return False
            else:
                return True
    if x>x_blue+85-36:
        overlap = y+72-y_blue
        y1=72-overlap
        
        for i in range(72,y1,-1):
            if x_blue<x+ball_coordinates[i][0]:
                contact=False
            else:
                contact=True
        return contact
    
def get_playerbpos(x,y,x_blue,y_blue,lr,side,tracker_x,movement):

    if movement=='l':
        change=-1
    else:
        change=1
    
    if side!=1:
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

        if y+72>=y_blue and y<y_blue: #when part of the ball is below the players top
            
            contact=checkcontact(x,y,x_blue,y_blue)
            print contact
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

        if y>=y_blue and y<y_blue+150:

            if lr==0:
                if x+72>=x_blue:
                    if change==-1:
                        return x_blue
                    else:
                        x_blue+=change
                        return x_blue
                else:
                    x_blue+=change
                    return x_blue
            
            if lr==1:
                if x+72>=x_blue:
                    if change==-1:
                        return x_blue
                    else:
                        x_blue+=change
                        return x_blue
                else:
                    x_blue+=change
                    return x_blue

            if lr==-1:
                if x<=x_blue+85:
                    if change==-1:
                        x_blue+=change
                        return x_blue
                    else:
                        return x_blue
                else:
                    x_blue+=change
                    return x_blue
            
def get_ballpos(x,y,angle,lr,ud):

    if lr==0:
        if angle==90:
            if ud==-1:
                y+=2
                return x,y,angle,ud,lr
            if ud==1:
                y-=2
                return x,y,angle,ud,lr
    return x,y,angle,ud,lr
                    
            
    



    
