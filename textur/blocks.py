def new_blocks():
    def grass():
        ba = dict(grass="new_blocks()[1]('grass_ba')(blocksname,buildPos,set_block)")
        da = dict(grass="")
        image_name = "gras_erde_block.png"
        item_name = "gras_item.png"
        return ba, da, image_name, item_name
    def wool():
        ba = dict(wool="")
        da = dict(wool="")
        image_name = "wolle_block.png"
        item_name = "wolle_item.png"
        return ba, da, image_name, item_name
    def seed():
        ba = dict(seed="")
        da = dict(seed="")
        image_name = "setzling.png"
        item_name = "setzling_item.png"
        return ba, da, image_name, item_name
############################################################
    def func_wrap(funcname):
        def grass_ba(blocksname,buildPos,set_block):
            set_block(blocksname,buildPos,'dirt')
        funcs = {"grass_ba":grass_ba}#<- put your new function in here
############################################################
        try:
            func = funcs[funcname]
        except:
            func = ""
            print "function wrapper: couldn't find function "+funcname
        return func
    all_new_blocks = [wool,seed]
    return all_new_blocks,func_wrap
