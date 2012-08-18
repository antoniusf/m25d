# -*- coding: utf-8 -*-
#Version 1.0!
import math, pygame, random, time
from pygame.locals import *
from blocks import new_blocks

def draw_block(window, block, (x,y,z)):
    """draws a block to a given position"""
    xd = 32*x-7*32 #calculate 2d-x (left-right) coordinate from 3d-x (left-right)
    yd = 216-(32*z+12) #calculate 2d-y (up-down) coordinate from 3d-z (up-down)
    xd += y*12 #add the "diagonal" 3d-y (spatial) to 2d-x and 2d-y
    yd -= y*12
    window.blit(block,(xd,yd))
    
def create_blocks():
    """loads all used block pngs as pygame image objects and return them in a tuple"""
    global grass;global dirt;global tree;global wood;global leaves;global sand;global gravel;global clay;global stone;global iron;global coal;global gold;global diamond;global none;global overlay;global head_front;global head_left;global head_back;global head_right
    grass = pygame.image.load('gras_erde_block.png')
    dirt = pygame.image.load('erde_block.png')
    tree = pygame.image.load('baum_block.png')
    wood = pygame.image.load('holz_block.png')
    leaves = pygame.image.load('blatt_block.png')
    sand = pygame.image.load('sand_block.png')
    gravel = pygame.image.load('schotter_block.png')
    clay = pygame.image.load('lehm_block.png')
    stone = pygame.image.load('stein_block.png')
    iron = pygame.image.load('eisen_block.png')
    coal = pygame.image.load('kohle_block.png')
    gold = pygame.image.load('gold_block.png')
    diamond = pygame.image.load('diamant_block.png')
    none = pygame.Surface((0,0))
    overlay = pygame.image.load('overlay.png')
    head_front = pygame.image.load('kopf-vorne.png')
    head_left = pygame.image.load('kopf-links.png')
    head_back = pygame.image.load('kopf-hinten.png')
    head_right = pygame.image.load('kopf-rechts.png')
    newblocknames = []
    nbnstr = []
    for elem in new_blocks()[0]:
        name = elem()[0].popitem()[0]
        exec(name+" = pygame.image.load('"+elem()[2]+"')")
        exec("newblocknames.append("+name+")")
        nbnstr.append(name)
    blocktypes = [grass,dirt,tree,wood,leaves,sand,gravel,clay,stone,iron,coal,gold,diamond,none,overlay,head_front,head_left,head_back,head_right]
    blocktypes.extend(newblocknames)
    return blocktypes,none,newblocknames,nbnstr

def create_items():
    """like create_blocks, just with items"""
    grassitem = pygame.image.load('gras_item.png')
    dirtitem = pygame.image.load('erde_item.png')
    treeitem = pygame.image.load('baum_item.png')
    wooditem = pygame.image.load('holz_item.png')
    leavesitem = pygame.image.load('blatt_item.png')
    sanditem = pygame.image.load('sand_item.png')
    gravelitem = pygame.image.load('schotter_item.png')
    clayitem = pygame.image.load('lehm_item.png')
    stoneitem = pygame.image.load('stein_item.png')
    ironitem = pygame.image.load('eisen_item.png')
    coalitem = pygame.image.load('kohle_item.png')
    golditem = pygame.image.load('gold_item.png')
    diamonditem = pygame.image.load('diamant_item.png')
    newitemnames = []
    ninstr = []
    for elem in new_blocks()[0]:
        name = elem()[0].popitem()[0]
        name += 'item'
        exec(name+"=pygame.image.load('"+elem()[3]+"')")
        exec("newitemnames.append("+name+")")
        ninstr.append(name[0:-4])
    itemtypes = [grassitem,dirtitem,treeitem,wooditem,leavesitem,sanditem,gravelitem,clayitem,stoneitem,ironitem,coalitem,golditem,diamonditem]
    itemtypes.extend(newitemnames)
    return itemtypes, ninstr

def update(window,blocksname):
    global blocks
    global diffPosx
    global diffPosy
    """draws all blocks in the right order (hidden blocks are not visible) and updates the screen"""
    window.fill((137,181,255))
    ymin = (-SCREENLENGTH)-diffPosy#damit y rückwärts zählt
    ymax = 1-diffPosy
    xmin = 0 + diffPosx
    xmax = SCREENWIDTH + 1 +diffPosx
    for y in range(ymin,ymax):
        for z in range(0,MAXHEIGHT):
            for x in range(xmin,xmax):
                yi = y*(-1)#damit y rückwärts zählt
                if blocksname[x][yi][z] == "dirt" and random.random() < 0.03:
                    if blocksname[x][yi][z+1] == "none":
                        blocksname[x][yi][z] = "grass"
                elif blocksname[x][yi][z] == "grass" and blocksname[x][yi][z+1] != "none":
                    b = blocksname[x][yi][z+1]
                    if b not in ["head_front","head_left","head_back","head_right"]:
                        blocksname[x][yi][z] = "dirt"
                blocktype = blocksname[x][yi][z]
                exec("i = blocktypes.index("+blocktype+")")
                blocktype = blocktypes[i]
                draw_block(window, blocktype, (x-diffPosx,yi-diffPosy,z))#diffPosy für das mitlaufen des bildes
    global hglpos
    global itempos
    update_itembar(itempos,hglpos)
    pygame.display.update()

def update_itembar(itempos,hglpos):
    """updates the itembar"""
    window.blit(itembar,(139,148))
    window.blit(highlight,(139+34*hglpos,148))
    if hglpos == 0:
        window.blit(itemsbar[itempos],(139+8,148+8))
        window.blit(itemsbar[itempos+1],(139+8+34,148+8))
        window.blit(itemsbar[itempos+2],(139+8+34*2,148+8))
    elif hglpos == 1:
        window.blit(itemsbar[itempos-1],(139+8,148+8))
        window.blit(itemsbar[itempos],(139+8+34,148+8))
        window.blit(itemsbar[itempos+1],(139+8+34*2,148+8))
    elif hglpos == 2:
        window.blit(itemsbar[itempos-2],(139+8,148+8))
        window.blit(itemsbar[itempos-1],(139+8+34,148+8))
        window.blit(itemsbar[itempos],(139+8+34*2,148+8))
    pygame.display.update()

def itembarshift(itempos,hglpos,dirc):
    """shifts all items to the left(dirc = 0) or right(dirc = 1)"""
    if dirc == 1:
        itempos += 1
    elif dirc == 0:
        itempos -= 1
    if itempos < 0:
        itempos = 0
    elif itempos >= NUMBEROFITEMS:
        itempos = NUMBEROFITEMS-1
    if itempos == 0:
        hglpos = 0
    elif itempos == NUMBEROFITEMS-1:
        hglpos = 2
    else: hglpos = 1
    update_itembar(itempos,hglpos)
    return itempos, hglpos

def build(ovPos,items,itempos,height):
    global viewdirc
    x = 0
    y = 0
    if height+ovPos[2] == 0: #if (height and ovPos) == 0; (height and ovPos[2] cant be negative
        height = 1
    if viewdirc == 0:
        y = 1
    elif viewdirc == 1:
        x = 1
    elif viewdirc == 2:
        y = -1
    elif viewdirc == 3:
        x = -1
    buildPos = (ovPos[0]+x,ovPos[1]+y,ovPos[2]+(height-1))
    block = items[itempos]
    if get_block(blocksname,buildPos) == "none":
        action = ba[block]
        if action != "":
            exec(action)
        else:
            set_block(blocksname,buildPos,block)
    else:
        action = da[block]
        if action != "":
            exec(action)
        else:
            set_block(blocksname,buildPos,"none")
    update(window,blocksname)

##def build_left(ovPos,items,itempos):
##    buildPos = (ovPos[0]-1,ovPos[1],ovPos[2])
##    set_block(blocksname,buildPos,items[itempos])
##    update(window,blocksname)
##
##def build_right(ovPos,items,itempos):
##    buildPos = (ovPos[0]+1,ovPos[1],ovPos[2])
##    set_block(blocksname,buildPos,items[itempos])
##    update(window,blocksname)
##
##def build_under(ovPos,items,itempos):
##    buildPos = (ovPos[0],ovPos[1],ovPos[2]-1)
##    set_block(blocksname,buildPos,items[itempos])
##    update(window,blocksname)

def sb(blocks,(x,y,z),blocktype,window):
	blocks[x][y][z] = blocktype
	update(window,blocks)

def set_block(blocks,(x,y,z),blocktype):
    blocksname[x][y][z] = blocktype

def get_block(blocksname,(x,y,z)):
    return blocksname[x][y][z]

def generate_blockslist(none):
    blocks = []
    for i in range(0,MAXWIDTH+1):
            blocks.append([][:])	
    for i in range(0,MAXWIDTH+1):
            for j in range(0,MAXLENGTH+1):
                    blocks[i].append([][:])
    for i in range(0,MAXWIDTH+1):
            for j in range(0,MAXLENGTH+1):
                    for k in range(0,MAXHEIGHT+1):
                            blocks[i][j].append(none)
    return blocks

def noise(x,y):
    random.seed(x+y*57+RANDOMNUMBER)
    number = random.random()
    return number

#def interpolate_bicubic(
def smooth_noise(x,y):
    number = noise(x,y)
    number1 = noise(x+1,y)
    number2 = noise(x,y+1)
    number3 = noise(x+1,y+1)
    number4 = noise(x-1,y)
    number5 = noise(x,y-1)
    number6 = noise(x-1,y-1)
    number7 = noise(x-1,y+1)
    number8 = noise(x+1,y-1)
    result = (1/4.0)*number #middle
    result += (1/8.0)*(number1+number2+number4+number5)#edges
    result += (1/16.0)*(number3+number6+number7+number8)#vertices
    return result

def perlinNoise(x,y):
    p = 1/10.0 #persistence
    o = 3 #octaves
    result = 0
    for i in range(0,o):
        f = 2**i #frequency
        a = p**i #amplitude
        result += smooth_noise(x*f,y*f)*a
    result2 = result
    result = round((round(result,1)-0.6)*10,0)
    if result < 0:
        result = 0.0
    if result > 3:
        result = 3.0
    return result,result2

def onp():
    print("operation not possible")

def move2(ovPos,newPos):
    def changeDP(ovPos):
        global diffPosx
        global diffPosy
        diffPosx = ovPos[0] - 9
        diffPosy = ovPos[1] - 9
    def set_viewdirc(viewdirc):
        if viewdirc == 0:
            ov = "head_back"
        elif viewdirc == 1:
            ov = "head_right"
        elif viewdirc == 2:
            ov = "head_front"
        elif viewdirc == 3:
            ov = "head_left"
        return ov
    global blocksname
    global viewdirc
    if get_block(blocksname,newPos) == "none":
        if get_block(blocksname,(newPos[0],newPos[1],newPos[2]-1)) == "none":
            if newPos[2] >= 1:
                newPos = newPos[0],newPos[1],newPos[2]-1
        set_block(blocksname,ovPos,"none")
        ovPos = newPos
        set_block(blocksname,ovPos,set_viewdirc(viewdirc))
        changeDP(ovPos)
        update(window,blocksname)
    elif get_block(blocksname,(newPos[0],newPos[1],newPos[2]+1)) == "none":
        if newPos[2] < MAXHEIGHT-1:
            newPos = (newPos[0],newPos[1],newPos[2]+1)
            set_block(blocksname,ovPos,"none")
            ovPos = newPos
            set_block(blocksname,ovPos,set_viewdirc(viewdirc))
            changeDP(ovPos)
            update(window,blocksname)
    else:
        onp()
    return ovPos

def move(ovPos,dirc):
    newPos = ovPos
    global viewdirc
    viewdirc = dirc
    if dirc == 0:
        if ovPos[1] < MAXLENGTH:
            newPos = ovPos[0],ovPos[1]+1,ovPos[2]
            ovPos = move2(ovPos,newPos) 
        else:
            onp()
    elif dirc == 1:
        if ovPos[0] < MAXWIDTH:
            newPos = ovPos[0]+1,ovPos[1],ovPos[2]
            ovPos = move2(ovPos,newPos) 
        else:
            onp()
    elif dirc == 2:
        if ovPos[1] > 0:
            newPos = ovPos[0],ovPos[1]-1,ovPos[2]
            ovPos = move2(ovPos,newPos) 
        else:
            onp()
    elif dirc == 3:
        if ovPos[0] > 0:
            newPos = ovPos[0]-1,ovPos[1],ovPos[2]
            ovPos = move2(ovPos,newPos) 
        else:
            onp()
    return ovPos

def shift(ovPos,dirc):
    global blocksname
    newPos = ovPos
    if dirc == 1:
        if ovPos[2] < MAXHEIGHT:
            newPos = ovPos[0],ovPos[1],ovPos[2]+1
            set_block(blocksname,ovPos,'none')
            set_block(blocksname,newPos,'overlay')
        else:
            print("operation not possible")
    elif dirc == 0:
        if ovPos[2] > 0:
            newPos = ovPos[0],ovPos[1],ovPos[2]-1
            set_block(blocksname,ovPos,'none')
            set_block(blocksname,newPos,'overlay')
        else:
            print("operation not possible")
    update(window,blocksname)
    return newPos

def getMainRandomNumber():
    random.seed(time.time())
    return random.random()

MAXWIDTH = 128
MAXLENGTH = 128
MAXHEIGHT = 4
SCREENWIDTH = 18
SCREENLENGTH = 18
diffPosx = 0
diffPosy = 0
RANDOMNUMBER = getMainRandomNumber()
viewdirc = 0
ba = {"grass":"","dirt":"","tree":"","wood":"","leaves":"","sand":"","gravel":"","clay":"","stone":"","iron":"","coal":"","gold":"","diamond":"","none":""}
da = {"grass":"","dirt":"","tree":"","wood":"","leaves":"","sand":"","gravel":"","clay":"","stone":"","iron":"","coal":"","gold":"","diamond":"","none":""}
newblocks = new_blocks()[0]
for elem in newblocks:
    ba.update(elem()[0])
    da.update(elem()[1])

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((384,216))#eigentlich 384*216
    #pygame.font.init()
    blocktypes,none,newblocknames,nbnstr = create_blocks()
    itemsbar,ninstr = create_items()
    itemsbar.append(none)
    itemsbar.append(none)
    for i in range(len(newblocknames)):
        exec(nbnstr[i]+"=newblocknames[i]")
    #blocks = generate_blockslist(none)
    blocks = None
    blocksname = generate_blockslist("none")
    ovPos = (9,9,1)
    gesamt = float((MAXLENGTH - 40)*(MAXWIDTH - 40))
    action = raw_input("[n (New Map)/o (Open Map)]")
    name = None
    print "LOADING"
    if action == "n":
        #window.blit(text2,(125,60)) --> LOADING
        for i in range(0,MAXWIDTH-40):
            for j in range(0,MAXLENGTH-40):
                height,bla = perlinNoise(i,j)
                height = int(height)
                bla = int(round(bla*100,0))
                if bla > 40 :
                    set_block(blocksname,(i,j,height),"grass")
                elif bla < 40 and bla > 37:
                    set_block(blocksname,(i,j,height),"clay")
                elif bla < 37 and bla > 30:
                    set_block(blocksname,(i,j,height),"sand")
                elif bla < 30:
                    set_block(blocksname,(i,j,height),"gravel")
                if height == 0:
                    if random.random() < 0.02:
                        set_block(blocksname,(i,j,height+1),"tree")
                        set_block(blocksname,(i,j,height+2),"tree")
                        set_block(blocksname,(i+1,j,height+2),"leaves")
                        set_block(blocksname,(i-1,j,height+2),"leaves")
                        set_block(blocksname,(i,j+1,height+2),"leaves")
                        set_block(blocksname,(i,j-1,height+2),"leaves")
                        set_block(blocksname,(i,j,height+3),"leaves")
                if height == 1:
                        set_block(blocksname,(i,j,height-1),"dirt")
                elif height == 2:
                    set_block(blocksname,(i,j,height-1),"dirt")
                    rand = random.random()
                    if rand > 0.5:
                        set_block(blocksname,(i,j,height-2),"stone")
                    elif rand > 0.4:
                        set_block(blocksname,(i,j,height-2),"coal")
                    elif rand > 0.1:
                        set_block(blocksname,(i,j,height-2),"iron")
                    elif rand < 0.1:
                        set_block(blocksname,(i,j,height-2),"gold")
            prozent = round(round((i*j)/gesamt,2)*100)
            print int(prozent),"%"
            #window.blit(text2b,(170,100)) --> ...%
    elif action == "o":
        name = raw_input("name of map: ")
        try:
            d = open(name,"r")
            exec("blocksname="+d.readline())
            exec("ovPos="+d.readline())
        except:
            print "reading fail. please check data format"
    else:
        print "non-valid key. exiting"
    set_block(blocks,ovPos,"head_back")
    diffPosx = ovPos[0] - 9
    diffPosy = ovPos[1] - 9
    itembar = pygame.image.load('itembar.png')
    highlight = pygame.image.load('highlight.png')
    hglpos = 0
    itempos = 0
    items = ["grass","dirt","tree","wood","leaves","sand","gravel","clay","stone","iron","coal","gold","diamond"]
    items.extend(ninstr)
    items.append("none")
    NUMBEROFITEMS = len(items)
    #itemsbar = [grassitem,dirtitem,treeitem,wooditem,leavesitem,sanditem,gravelitem,clayitem,stoneitem,ironitem,coalitem,golditem,diamonditem,none,none]
    #window.blit(itembar,(247,332)) #siehe weiter oben in update
    #window.blit(highlight,(247+34,332)) #fuer items: plus 8 (x und y); weiter links plus 34
    update(window,blocksname)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                if pygame.font.get_init:
                    pygame.font.quit()
                if name != None:
                    print "SAVING"
                    a = str(blocksname)
                    d = open(name,"w")
                    d.write(a)
                    d.write("\n")
                    d.write(str(ovPos))
                    d.close()
                elif name == None:
                    a = str(blocksname)
                    dname = raw_input("enter name for world: ")
                    d = open(dname,"w")
                    print "SAVING"
                    d.write(a)
                    d.write("\n")
                    d.write(str(ovPos))
                    d.close()
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    ovPos = move(ovPos,0)
                if event.key == K_DOWN:
                    ovPos = move(ovPos,2)
                if event.key == K_RIGHT:
                    ovPos = move(ovPos,1)
                if event.key == K_LEFT:
                    ovPos = move(ovPos,3)
                if event.key == K_c:
                    itempos,hglpos = itembarshift(itempos,hglpos,1)
                if event.key == K_y:
                    itempos,hglpos = itembarshift(itempos,hglpos,0)
                if event.key == K_w:
                    build(ovPos,items,itempos,1)
                if event.key == K_a:
                    build(ovPos,items,itempos,2)
                if event.key == K_d:
                    build(ovPos,items,itempos,0)
##                if event.key == K_s:
##                    build_under(ovPos,items,itempos)
                if event.key == K_r:
                    ovPos = shift(ovPos,1)
                if event.key == K_f:
                    ovPos = shift(ovPos,0)
            elif event.type == KEYUP:
                if event.key == K_w and (event.mod == KMOD_LCTRL or event.mod == KMOD_RCTRL):
                    pygame.event.post(pygame.event.Event(QUIT))

