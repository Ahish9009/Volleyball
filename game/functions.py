import pygame as pg

#to load images
def load_images():
    
    bg=pg.image.load('pictures/bg.png')
    rod=pg.image.load('pictures/rod.png')
    playerr=pg.image.load('pictures/player red.jpg')
    playerb=pg.image.load('pictures/player blue.jpg')
    volleyball=pg.image.load('pictures/volleyball.png')

#to transform image sizes
def transform_images():
    
    bg=pg.transform.scale(bg, (600,600))
    rod=pg.transform.scale(rod, (14,300))
    playerr=pg.transform.scale(playerr, (85,150))
    playerb=pg.transform.scale(playerb, (85,150))
    volleyball=pg.transform.scale(volleyball, (72,72)) #r=36

#to invert direction horizontally
def invert_lr(lr):
    lr*=(-1)
    return lr

#to invert direction vertially
def invert_ud(ud):
    ud*=(-1)
    return ud
