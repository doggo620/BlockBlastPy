import pygame as pg
import random
import blocklib
import cv2
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#init pygame module
pg.init()
pg.font.init()

#icon 
img = pg.image.load(resource_path("icon.png"))
#subway surf
video = cv2.VideoCapture(resource_path("video.mp4"))
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)

mapa = blocklib.map()
#1290
screen = pg.display.set_mode((1200,800))
pg.display.set_caption("BlockBlast Ultima")
pg.display.set_icon(img)
clock = pg.time.Clock()
running = True

#font stuff
my_font = pg.font.SysFont('Comic Sans MS', 100)

score = 0
blocks: list[blocklib.Shape] = []

bg_color = (0,0,0)


while running:
    
    if len(blocks) == 0:

        blocks = blocklib.genBlocks(mapa)

    score_text = my_font.render(str(score), True, (0, 0, 0))
    #event handler
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False

    #background
    new = []
    for i in range(3):
        if bg_color[i] >= 255:
            new.append(0)
        else:
            new.append(bg_color[i])

    bg_color = (tuple(new))
    bg_color = (bg_color[0] + random.randint(0,1),bg_color[1] + random.randint(0,1), bg_color[2] + random.randint(0,1))
    screen.fill(bg_color)

    mapa.render(screen)

    #subways surf render
    success, video_image = video.read()
    if success:
        video_surf = pg.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
        screen.blit(video_surf, (mapa.size[0] * blocklib.block_size + 10, 0))
    else:
        video = cv2.VideoCapture(resource_path("video.mp4"))
    
    screen.blit(score_text, (mapa.size[0] * blocklib.block_size + 260,blocklib.block_size * mapa.size[1] + 60))
    #mapa.size[0] * blocklib.block_size + 10, 0

    #keyboard handling
    keys = pg.key.get_pressed()

    #TODO: Delete debuging help
    #debugging
    if keys[pg.K_UP]:
        for sh in blocks:
            print(mapa.getAvaliable(sh))
    if keys[pg.K_DOWN]:
        print(blocklib.checkPossibility(mapa, blocks))
    if keys[pg.K_r]:
        score = 0
        mapa.reset()
        blocks = []
        my_font = pg.font.SysFont('Comic Sans MS', 100)
    if keys[pg.K_RIGHT]:
        xd = blocklib.checkPossibility(mapa, blocks)
        if xd[0]:
            if (blocklib.mapPlaceAuto(0,0,xd[1][0][1][0],xd[1][0][1][1],xd[1][0][0], mapa)):
                blocks.remove(xd[1][0][0])
                if not blocklib.checkPossibility(mapa, blocks)[0]:
                    pass
                    #print(blocklib.checkPossibility(mapa, blocks)[1])


    #mouse position
    p = pg.mouse.get_pos()

    #check for picked block
    pickedUp: blocklib.Shape = blocklib.checkPicked(blocks)

    if pickedUp:
        blocklib.mapPlaceCheck(p[0],p[1],pickedUp, mapa)
        pickedUp.update(p[0],p[1])

    #mouse press event
    mPressed = pg.mouse.get_pressed()[0]
    if mPressed:
        #activate block and save offsets
        if not pickedUp:
            for block in blocks:
                if block.picked == False and block.checkClick(p[0], p[1]):
                    block.picked = True
    else:
        #disable the block
        #TODO: in original game go back to original position
        #pickedUp: blocklib.Shape = blocklib.checkPicked(blocks)
        if pickedUp:
            pickedUp.picked = False
            if (blocklib.mapPlace(p[0],p[1],pickedUp, mapa)):
                blocks.remove(pickedUp)
                try:
                    score += blocklib.checkWin(mapa)
                except:
                    pass
                if not blocklib.checkPossibility(mapa, blocks)[0]:
                    #print(blocklib.checkPossibility(mapa, blocks)[1])
                    score = "GAME OVER ES"
                    my_font = pg.font.SysFont('Comic Sans MS', 50)
                    #mapa.reset()
                    #blocks = []
                    #mapa.print()
            else:
                pickedUp.offset = (0,0,0,0)
                pickedUp.update(pickedUp.origin[0], pickedUp.origin[1])

    #move the block if activated
    #pickedUp: blocklib.Shape = blocklib.checkPicked(blocks)

    #draw every block
    for block in blocks:
        block.render(screen)
    try:
        score += blocklib.checkWin(mapa)
    except:
        pass

    #flush the screen
    pg.display.flip()

    #fps cap
    clock.tick(60)

pg.quit()