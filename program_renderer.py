import pygame
class renderer:
    def __init__(self, screen, program,position):
        # initialise varaibles
        self.position = position
        self.program = program
        self.screen = screen
        self.running = True
        self.selected = None
        self.selected_anchor = None
        self.scroll = 0
        self.height = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.rects = []
        self.new_program = []
    def tick(self,events):
        # this function is called every frame.
        # it calls the renderer and handles inputs
        for event in events: # event handling loop (no need for quit event, handled by main)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # LMB click
                    mouse_pos = pygame.mouse.get_pos() 
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
            if event.type == pygame.MOUSEBUTTONUP:
                #release click
                if event.button == 1:
                    self.selected = None
                    self.program = self.new_program
                    #apply changes, set new program
        self.render_program() # run render program
        pygame.draw.rect(self.screen, (255,255,255), (0,self.screen.get_height()-100,self.screen.get_width(),100)) # draw white box at bottom for other stuff
        return self.program
    def render_program(self):
        x,y = self.position # position extraction for less typing
        offset = 0
        indentLevel = 0
        selectIndentLevel = 0
        selectOffset = 0
        indentColor = (150,150,0) # indent color, really should be a list, but this is fine for now
        mouse_pos = pygame.mouse.get_pos()

        startIndex = self.selected
        endIndex = self.selected + 1 if self.selected is not None else None

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
            text = self.font.render(block.toText(), False, (0, 0, 0)) # get the text so we can render it and get its width to ensure it will fit
            width = text.get_width()
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
                if block.startIndent: # if the block is the start of an indent, render the indent. only visible if no blocks are inside the indent
                    pygame.draw.rect(self.screen, block.color, (mouse_pos[0]-self.selected_anchor[0]+x_offset,mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset,10,50))

                self.screen.blit(text,(20+mouse_pos[0]-self.selected_anchor[0]+x_offset,mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset)) # draw the text 
                for i in range(indentLevel): # draw the indents
                    if i < selectIndentLevel:
                        pygame.draw.rect(self.screen, indentColor, (x+i*20,y+offset-10,10,60)) # indents that are not being moved by the user
                    else:
                        # indents that are being moved by the user
                        pygame.draw.rect(self.screen, indentColor, (mouse_pos[0]-self.selected_anchor[0]+(i-selectIndentLevel)*20,mouse_pos[1]-self.selected_anchor[1] + offset + selectOffset -10,10,60))
            else:
                # draw the block
                pygame.draw.rect(self.screen, block.color, (x+x_offset,y+offset,max(200,width+40),40))
                if block.startIndent: # if the block is the start of an indent, render the indent. only visible if no blocks are inside the indent
                    pygame.draw.rect(self.screen, block.color, (x+x_offset,y+offset,10,50))
                self.screen.blit(text,(x+x_offset+20,y+offset)) # draw the text
                for i in range(indentLevel): # draw the indents
                    pygame.draw.rect(self.screen, indentColor, (x+i*20,y+offset-10,10,60))
            self.rects.append(pygame.Rect(x+x_offset,y+offset,max(200,width+40),40)) # add the rect to the list so we can check if the mouse is over it
            offset += 50 # move down 50 pixels
            if block.startIndent: 
                indentLevel += 1 # increase the indent level after rendering it (so it will render correctly)
        self.height = offset # set the height ( used for scrolling)