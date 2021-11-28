import pygame
from blockMaker import *
from arrow import *
import colorsys
import random
def randomRGB():
    h = random.random()
    s = 0.5
    v = 0.5
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
def saturateRGB(color, saturateAmount):
    return (min(255, max(0, color[0] * saturateAmount)), min(255, max(0, color[1] * saturateAmount)), min(255, max(0, color[2] * saturateAmount)))

class renderer:
    def __init__(self, screen, program, position, runner):
        # initialise varaibles
        self.runner = runner
        self.position = position
        self.program = program
        self.screen = screen
        self.running = True
        self.selected = None
        self.selected_anchor = None
        self.scroll = 0
        self.height = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.fontSmall = pygame.font.SysFont('Comic Sans MS', 20)
        self.rects = []
        self.new_program = []
        self.multiSelectRects = []
        self.openSelector = None
        self.multi_select_args = None
        self.multi_select_rects = []
        self.multi_select_values = []
        self.multi_select_block_index = None
        self.multi_select_index = None
        self.multi_add_rect = None
        self.multi_sub_rect = None
        self.multi_int_val = 0
    def tick(self,events):
        # this function is called every frame.
        # it calls the renderer and handles inputs
        for event in events: # event handling loop (no need for quit event, handled by main)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.openSelector == None:
                    if event.button == 3:
                        for n,i in enumerate(self.multiSelectRects):
                            if i.collidepoint(event.pos):
                                self.openSelector = n
                    if event.button == 1: # LMB click
                        for i,rect in enumerate(self.rects): 
                            if rect.collidepoint(mouse_pos) and mouse_pos[1] < self.screen.get_height() - 100: # check if mouse click is on a block (and that block is rendering)
                                if self.program[i].endIndent: # if the block is an end indent, do nothing, as it would take too much effort to implement
                                    pass
                                else:
                                    self.selected_anchor = (mouse_pos[0]-rect.x,mouse_pos[1]-rect.y) # set anchor point (where on the block the click happened)
                                    self.selected = i # set selected block
                    if event.button == 4:
                        #scroll up
                        self.scroll = max(0,self.scroll-50)
                    if event.button == 5:
                        #scroll down
                        self.scroll = min(self.height-(self.screen.get_height()-100),self.scroll+50)
                else:
                    close = True
                    if self.multi_add_rect and self.multi_add_rect.collidepoint(mouse_pos):
                        self.multi_int_val += 1
                        self.multi_int_val %= 100
                        close = False
                    if self.multi_sub_rect and self.multi_sub_rect.collidepoint(mouse_pos):
                        self.multi_int_val -= 1
                        self.multi_int_val %= 100
                        close = False
                    for v,i in enumerate(self.multi_select_rects):
                        if i.collidepoint(event.pos):
                            if self.multi_select_values[v] == "number":
                                self.multi_select_values[v] = self.multi_int_val
                            self.program[self.multi_select_block_index].setMultiSelect(self.multi_select_index, self.multi_select_values[v])
                            break
                    if close:
                        self.openSelector = None
            if event.type == pygame.MOUSEBUTTONUP:
                #release click
                if event.button == 1:
                    self.selected = None
                    self.program = self.new_program
                    #apply changes, set new program
        self.render_program() # run render program
        pygame.draw.rect(self.screen, (255,255,255), (0,self.screen.get_height()-100,self.screen.get_width(),100)) # draw white box at bottom for other stuff
        return self.program
    def render_multi_select(self, position, place, current, color=(255,255,255), render_dropdown = False,block=None,index = None):

        if place == "if_value":
            options = self.runner.get_valid_values(None) + ["number"]
        elif place == "if_op":
            options = ["==","!=",">","<",">=","<="]
        elif place == "jump":
            options = ["number"]
        else:
            raise ValueError(f"invalid place {place}")
        if render_dropdown:
            self.multi_select_rects = []
            self.multi_select_values = []
            y_offset = 0
            for i in options:
                y_offset += 30
                if i == "number":
                    text = self.fontSmall.render(str(self.multi_int_val).zfill(2), True, (0,0,0))
                    add = self.fontSmall.render("+", True, (0,0,0))
                    sub = self.fontSmall.render("-", True, (0,0,0))
                    pygame.draw.rect(self.screen, color, (position[0],position[1]+y_offset,30+add.get_width()+sub.get_width()+40,30))
                    self.screen.blit(text, (position[0]+10,position[1]+y_offset))
                    self.screen.blit(add, (position[0]+20+30,position[1]+y_offset))
                    self.screen.blit(sub, (position[0]+30+30+add.get_width(),position[1]+y_offset))
                    self.multi_add_rect = pygame.Rect(position[0]+20+30,position[1]+y_offset,add.get_width(),30)
                    self.multi_sub_rect = pygame.Rect(position[0]+30+30+add.get_width(),position[1]+y_offset,sub.get_width(),30)
                    self.multi_select_rects.append(pygame.Rect(position[0],position[1]+y_offset,50,30))
                    self.multi_select_values.append(i)
                else:
                    text = self.fontSmall.render(i, True, (0,0,0))
                    pygame.draw.rect(self.screen, color, (position[0],position[1]+y_offset,text.get_width()+20,30))
                    self.screen.blit(text, (position[0]+10,position[1]+y_offset))
                    self.multi_select_rects.append(pygame.Rect(position[0],position[1]+y_offset,text.get_width()+20,30))
                    self.multi_select_values.append(i)
                    self.multi_add_rect = None
                    self.multi_sub_rect = None

            return
        text = self.fontSmall.render(str(current), True, (0,0,0))
        pygame.draw.rect(self.screen, color, (position[0],position[1],text.get_width()+20,30))
        self.screen.blit(text, (position[0]+10,position[1]))
        if self.openSelector is not None:
            if len(self.multiSelectRects) == self.openSelector:
                self.multi_select_args = (position,place,current,color,True)
                self.multi_select_block_index = self.program.index(block)
                self.multi_select_index = index
                
        self.multiSelectRects.append(pygame.Rect(position[0],position[1],text.get_width()+20,30))
    def get_multi_select_width(self,current):

        text = self.fontSmall.render(str(current), True, (0,0,0))
        return text.get_width()+20
    def render_block_label(self, position, label,block, color=(255,255,255)):
        x_pos = 0
        for i in label:
            if type(i) == BlockLabelText:
                text = self.font.render(i.text, True, (0,0,0))
                self.screen.blit(text, (position[0]+x_pos,position[1]-10))
                x_pos += text.get_width()+10
            if type(i) == BlockLabelMultiSelect:
                self.render_multi_select((position[0]+x_pos,position[1]), i.place, block.multiSelect[i.index],color,block=block, index = i.index)
                x_pos += self.get_multi_select_width(block.multiSelect[i.index])+10
    def get_block_label_width(self, label, block):
        x_pos = 0
        for i in label:
            if type(i) == BlockLabelText:
                text = self.font.render(i.text, True, (0,0,0))
                x_pos += text.get_width()+10
            if type(i) == BlockLabelMultiSelect:
                x_pos += self.get_multi_select_width(block.multiSelect[i.index])+10
        return x_pos
    def render_program(self):
        self.multi_select_args = None
        x,y = self.position # position extraction for less typing
        offset = 0
        indentLevel = 0
        selectIndentLevel = 0
        selectOffset = 0
        end_of_blocks = []
        indentColor = (150,150,0) # indent color, really should be a list, but this is fine for now
        mouse_pos = pygame.mouse.get_pos()
        renderOpenMultiSelectArgs = []
        startIndex = self.selected
        endIndex = self.selected + 1 if self.selected is not None else None
        self.multiSelectRects = []
        if self.selected is not None:
            newIndex = (mouse_pos[1] - self.position[1])//50 # get the index of the block the mouse is over (which is where we want to insert the selected block)
            if self.program[startIndex].startIndent: # if the selected block is the start of an indented section, we need to find the end of the indented section
                #to move the whode section
                indent = 1
                while indent:
                    if endIndex >= len(self.program):
                        break
                    if self.program[endIndex].startIndent:
                        indent += 1
                    elif self.program[endIndex].endIndent:
                        indent -= 1
                    endIndex += 1
                #endIndex is now the index of the end of the indented section (+1)
                if newIndex - startIndex + endIndex > len(self.program): # if the moved blocks would be outside the program bounds, this causes visual bugs, so we 
                    # move the end of the selection to the end of the program
                    newIndex = len(self.program) - (endIndex - startIndex)
            self.new_program = self.program.copy() # make a copy of the program
            selected_block = self.new_program[startIndex:endIndex] # store the selected blocks
            self.new_program = self.new_program[:startIndex] + self.new_program[endIndex:] # remove the selected blocks 
            self.new_program[newIndex:newIndex] = selected_block # insert the selected blocks at the new index
            startIndex, endIndex = newIndex, newIndex + (endIndex-startIndex) # update the start and end index of the selected blocks now they are moved
        else:
            self.new_program = self.program.copy() # make a copy of the program because the rest of the function uses the new program variable
        self.rects = [] # clear the rects list
        for i,block in enumerate(self.new_program): # iterate through the program
            width = self.get_block_label_width(block.toShowOnBlock(),block)
            if block.endIndent:
                indentLevel -= 1 # decrease the indent level before rendering it (so it will render correctly)

            x_offset = indentLevel*20 # get offset due to indent level
            if i == startIndex: # if the block is the start of the selected block, set a couple variables
                selectOffset = - offset # to remove the offset from how far it is down the program, while keeping the relative offset
                selectIndentLevel = indentLevel # to render the indents at the correct positions
            if startIndex is not None and i >= startIndex and i < endIndex: # if the block is being selected
                x_offset = (indentLevel-selectIndentLevel)*20 # set x offset because now we don't care about indents outside the selection
                pygame.draw.rect(self.screen, block.color,# draw the block
                    (mouse_pos[0] - self.selected_anchor[0] + x_offset, # x is at the cursor, but offset by the anchor point so when initially selected,
                    #the block doesn't move
                    mouse_pos[1] - self.selected_anchor[1] + offset + selectOffset, # same with y
                    max(200,width+40), # blocks are at least 200 pixels wide but longer if they need to fit more text
                    40)) # blocks are 40 pixels tall (with 10px gap)
                end_of_blocks.append((mouse_pos[0] - self.selected_anchor[0] + x_offset+max(200,width+40),mouse_pos[1] - self.selected_anchor[1] + offset + selectOffset+20))
                if block.startIndent: # if the block is the start of an indent, render the indent. only visible if no blocks are inside the indent
                    pygame.draw.rect(self.screen, block.color, (mouse_pos[0]-self.selected_anchor[0]+x_offset,mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset,10,50))
                self.render_block_label((mouse_pos[0]-self.selected_anchor[0]+x_offset+5,5+mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset),block.toShowOnBlock(),block,saturateRGB(block.color,1.5))
                for i in range(indentLevel): # draw the indents
                    if i < selectIndentLevel:
                        pygame.draw.rect(self.screen, indentColor, (x+i*20,y+offset-10,10,60)) # indents that are not being moved by the user
                    else:
                        # indents that are being moved by the user
                        pygame.draw.rect(self.screen, indentColor, (mouse_pos[0]-self.selected_anchor[0]+(i-selectIndentLevel)*20,mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset -10,10,60))
            else:
                # draw the block
                pygame.draw.rect(self.screen, block.color, (x+x_offset,y+offset,max(200,width+40),40))
                end_of_blocks.append((x+x_offset+max(200,width+40),y+offset+20))
                if block.startIndent: # if the block is the start of an indent, render the indent. only visible if no blocks are inside the indent
                    pygame.draw.rect(self.screen, block.color, (x+x_offset,y+offset,10,50))
                self.render_block_label((x+x_offset+25,y+offset+5),block.toShowOnBlock(),block,saturateRGB(block.color,1.5))
                
                for i in range(indentLevel): # draw the indents
                    pygame.draw.rect(self.screen, indentColor, (x+i*20,y+offset-10,10,60))
            self.rects.append(pygame.Rect(x+x_offset,y+offset,max(200,width+40),40)) # add the rect to the list so we can check if the mouse is over it
            offset += 50 # move down 50 pixels
            if block.startIndent: 
                indentLevel += 1 # increase the indent level after rendering it (so it will render correctly)
        self.height = offset # set the height ( used for scrolling)
        random.seed(5)
        for i,block in enumerate(self.new_program):
            if block.prefix == "jump":
                draw_arrow(screen, end_of_blocks[i], end_of_blocks[block.jumpLoc], 400, color = randomRGB())
        if self.multi_select_args:
            self.render_multi_select(*self.multi_select_args)