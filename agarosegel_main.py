import pygame as p
import ctypes,math,PIL
### init
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
p.init()
gel_img=p.image.load('agarosegel.jpg')
gel_img_size=gel_img.get_rect()
screenx=int(screensize[0]*0.8)
screeny=int(screensize[1]*0.85)
analysis_columnx=int(screensize[0]*0.10)
screen=p.display.set_mode((screenx,screeny))
p.display.set_caption('Agarose Gel')
if ((screenx-analysis_columnx)/screeny)>(gel_img_size[2]/gel_img_size[3]):
    gel_img=p.transform.scale(gel_img,(math.floor(screeny/gel_img_size[3])*gel_img_size[2],screeny))
else:
    gel_img=p.transform.scale(gel_img,((screenx-analysis_columnx),math.floor(screenx/gel_img_size[2])*gel_img_size[3]))
#####
### colours
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
#####
### vars
lines=[[0,0,-1]]
colours=[]
linetype=0
liner_mode=0
#####
### main funcs
def refresh():
    screen.blit(gel_img,(0,0))
    p.draw.rect(screen,(255,255,255),(screenx-analysis_columnx,0,analysis_columnx,screeny))
    p.display.update()
def display_liner(lines):
    refresh()
    for line in lines:
        if line[2]==0:
            p.draw.line(screen,RED,[0,line[1]],[screenx-analysis_columnx,line[1]],1)
        elif line[2]==1:
            p.draw.line(screen,GREEN,[line[0],0],[line[0],lines[1][1]+10],2)
    p.display.update()
def liner_find(position,lines):
    for line in lines:
        if line[2]==1:
            columnx=line[0]
    pixelvals=[]
    for x in range(0,13):
        pixel_colour=screen.get_at((columnx,position[1]-6+x))
        pixel_colour_magnitude=pixel_colour[0]+pixel_colour[1]+pixel_colour[2]
        pixelvals.append(pixel_colour_magnitude)
    value_1=pixelvals[0]
    pixelvals_differ=[]
    for i in range(1,13):
        pixelvals_differ.append(abs(value_1-pixelvals[i]))
        value_1=pixelvals[i]
    highest_difference_index=0
    highest_difference=0
    for z in range(0,12):
        if pixelvals_differ[z]>highest_difference:
            highest_difference=pixelvals_differ[z]
            highest_difference_index=z
    return (position[1]-6+highest_difference_index)

#####
### selection loop
active=True
refresh()
while active:
     for event in p.event.get():
        if event.type == p.QUIT:
            active=False
            p.quit()
        elif event.type == p.MOUSEBUTTONDOWN:
            position=event.pos
            if position[0]<screenx-analysis_columnx:
                if len(lines)==1:
                    filler=[position[0],position[1],0]
                    lines.append(filler)
                    liner_mode=1
                elif len(lines)==2:
                    filler=[position[0],position[1],1]
                    lines.append(filler)
                    liner_mode=0
                elif len(lines)>2:
                    if liner_mode==0:
                        filler=[position[0],liner_find(position,lines),0]
                        lines.append(filler)
                    elif liner_mode==1:
                        filler=[position[0],position[1],1]
                        lines.append(filler)
                        liner_mode=0
                display_liner(lines)
        elif event.type == p.KEYDOWN:
            key=event.key
            if key==p.K_SPACE:
                if liner_mode==0:
                    liner_mode=1
                else:
                    liner_mode=0
                display_liner(lines)
            elif key==p.K_k:
                active=False
        if liner_mode==1:
            if event.type == p.MOUSEMOTION:
                position=event.pos
                if position[0]<screenx-analysis_columnx:
                    display_liner(lines)
                    p.draw.line(screen,GREEN,[position[0],0],[position[0],lines[1][1]+10],2)
                    p.display.update()
print(lines)
            
#####
### analysis loop

#####



