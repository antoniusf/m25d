import pygame
from pygame.locals import *

def draw_block(window, block, (x,y,z)):
    """draws a block to a given position"""
    xd = 64*x #calculate 2d-x (left-right) coordinate from 3d-x (left-right)
    yd = 400-(64*z+24) #calculate 2d-y (up-down) coordinate from 3d-z (up-down)
    xd += y*24 #add the "diagonal" 3d-y (spatial) to 2d-x and 2d-y
    yd -= y*24
    window.blit(block,(xd,yd))
    
def create_blocks():
    """loads all used block pngs as pygame image objects and return them in a tuple"""
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
    redstone = pygame.image.load('redstone_block.png')
    diamond = pygame.image.load('diamant_block.png')
    lapis = pygame.image.load('lapis_block.png')
    none = pygame.Surface((0,0))
    overlay = pygame.image.load('overlay.png')
    return grass,dirt,tree,wood,leaves,sand,gravel,clay,stone,iron,coal,gold,redstone,diamond,lapis,none,overlay

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
    redstoneitem = pygame.image.load('redstone_item.png')
    diamonditem = pygame.image.load('diamant_item.png')
    lapisitem = pygame.image.load('lapis_item.png')
    return grassitem,dirtitem,treeitem,wooditem,leavesitem,sanditem,gravelitem,clayitem,stoneitem,ironitem,coalitem,golditem,redstoneitem,diamonditem,lapisitem

def update(window,blocks):
    """draws all blocks in the right order (hidden blocks are not visible) and updates the screen"""
    window.fill((137,181,255))
    for y in range(-MAXLENGTH,1):
        for z in range(0,MAXHEIGHT):
            for x in range(0,MAXWIDTH):
                yi = y*(-1)
                blocktype = blocks[x][yi][z]
                draw_block(window, blocktype, (x,yi,z))
    global hglpos
    global itempos
    update_itembar(itempos,hglpos)
    pygame.display.update()

def update_itembar(itempos,hglpos):
    """updates the itembar"""
    window.blit(itembar,(247,332))
    window.blit(highlight,(247+34*hglpos,332))
    if hglpos == 0:
        window.blit(itemsbar[itempos],(247+8,332+8))
        window.blit(itemsbar[itempos+1],(247+8+34,332+8))
        window.blit(itemsbar[itempos+2],(247+8+34*2,332+8))
    if hglpos == 1:
        window.blit(itemsbar[itempos-1],(247+8,332+8))
        window.blit(itemsbar[itempos],(247+8+34,332+8))
        window.blit(itemsbar[itempos+1],(247+8+34*2,332+8))
    if hglpos == 2:
        window.blit(itemsbar[itempos-2],(247+8,332+8))
        window.blit(itemsbar[itempos-1],(247+8+34,332+8))
        window.blit(itemsbar[itempos],(247+8+34*2,332+8))
        update(window,blocks)
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

def build_top(ovPos,items,itempos):
    buildPos = (ovPos[0],ovPos[1]+1,ovPos[2])
    set_block(blocks,buildPos,items[itempos])
    update(window,blocks)

def build_left(ovPos,items,itempos):
    buildPos = (ovPos[0]-1,ovPos[1],ovPos[2])
    set_block(blocks,buildPos,items[itempos])
    update(window,blocks)

def build_right(ovPos,items,itempos):
    buildPos = (ovPos[0]+1,ovPos[1],ovPos[2])
    set_block(blocks,buildPos,items[itempos])
    update(window,blocks)

def build_under(ovPos,items,itempos):
    buildPos = (ovPos[0],ovPos[1],ovPos[2]-1)
    set_block(blocks,buildPos,items[itempos])
    update(window,blocks)

def sb(blocks,(x,y,z),blocktype,window):
	blocks[x][y][z] = blocktype
	update(window,blocks)

def set_block(blocks,(x,y,z),blocktype):
    blocks[x][y][z] = blocktype

def get_block(blocks,(x,y,z)):
    return blocks[x][y][z]

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

def onp():
    print("operation not possible")

def move2(ovPos,newPos):
    global blocks
    if get_block(blocks,newPos) == none:
        if get_block(blocks,(newPos[0],newPos[1],newPos[2]-1)) == none:
            if newPos[2] >= 1:
                newPos = newPos[0],newPos[1],newPos[2]-1
        set_block(blocks,ovPos,none)
        ovPos = newPos
        set_block(blocks,ovPos,overlay)
        update(window,blocks)
    elif get_block(blocks,(newPos[0],newPos[1],newPos[2]+1)) == none:
        if newPos[2] < MAXHEIGHT:
            newPos = (newPos[0],newPos[1],newPos[2]+1)
            set_block(blocks,ovPos,none)
            ovPos = newPos
            set_block(blocks,ovPos,overlay)
            update(window,blocks)
    else:
        onp()
    return ovPos

def move(ovPos,dirc):
    newPos = ovPos
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
    global blocks
    newPos = ovPos
    if dirc == 1:
        if ovPos[2] < MAXHEIGHT:
            newPos = ovPos[0],ovPos[1],ovPos[2]+1
            set_block(blocks,ovPos,none)
            set_block(blocks,newPos,overlay)
        else:
            print("operation not possible")
    elif dirc == 0:
        if ovPos[2] > 0:
            newPos = ovPos[0],ovPos[1],ovPos[2]-1
            set_block(blocks,ovPos,none)
            set_block(blocks,newPos,overlay)
        else:
            print("operation not possible")
    update(window,blocks)
    return newPos

NUMBEROFITEMS = 16
MAXWIDTH = 11
MAXLENGTH = 11
MAXHEIGHT = 5

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600,400))
    grass,dirt,tree,wood,leaves,sand,gravel,clay,stone,iron,coal,gold,redstone,diamond,lapis,none,overlay = create_blocks()
    grassitem,dirtitem,treeitem,wooditem,leavesitem,sanditem,gravelitem,clayitem,stoneitem,ironitem,coalitem,golditem,redstoneitem,diamonditem,lapisitem = create_items()
    blocks = generate_blockslist(none)
    ovPos = (0,0,1)
    for i in range(0,MAXWIDTH):
        for j in range(0,MAXLENGTH):
            set_block(blocks,(i,j,0),grass)
    set_block(blocks,ovPos,overlay)
    itembar = pygame.image.load('itembar.png')
    highlight = pygame.image.load('highlight.png')
    hglpos = 0
    itempos = 0
    items = [grass,dirt,tree,wood,leaves,sand,gravel,clay,stone,iron,coal,gold,redstone,diamond,lapis,none]
    itemsbar = [grassitem,dirtitem,treeitem,wooditem,leavesitem,sanditem,gravelitem,clayitem,stoneitem,ironitem,coalitem,golditem,redstoneitem,diamonditem,lapisitem,none,none]
    #window.blit(itembar,(247,332)) #siehe weiter oben in update
    #window.blit(highlight,(247+34,332)) #fuer items: plus 8 (x und y); weiter links plus 34
    update(window,blocks)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
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
                    build_top(ovPos,items,itempos)
                if event.key == K_a:
                    build_right(ovPos,items,itempos)
                if event.key == K_d:
                    build_left(ovPos,items,itempos)
                if event.key == K_s:
                    build_under(ovPos,items,itempos)
                if event.key == K_r:
                    ovPos = shift(ovPos,1)
                if event.key == K_f:
                    ovPos = shift(ovPos,0)
