import colorsys
import random
import blocks
import pygame

from arrow import *
from blockMaker import *


def randomRGB(seed = None):
    if seed is not None:
        random.seed(seed)
    h = random.random()
    s = 0.5
    v = 0.5
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
def saturateRGB(color, saturateAmount):
    return (min(255, max(0, color[0] * saturateAmount)), min(255, max(0, color[1] * saturateAmount)), min(255, max(0, color[2] * saturateAmount)))

class renderer:
    # stuff here is for rendering
    def __init__(self, screen, blockList, usable_blocks,/,**kwargs):
        self.init_runner(**kwargs)
        self.blocks = blockList
        self.clock = pygame.time.Clock()
        self.empty_block_rects = {}
        self.font = pygame.font.SysFont('Arial', 30)
        self.font_small = pygame.font.SysFont('Arial', 20)
        self.height = 0
        self.multi_add_rect = None
        self.multi_int_val = 0
        self.multi_max_val = 100
        self.multi_min_val = 0
        self.multi_select_args = None
        self.multi_select_block = None
        self.multi_select_index = None
        self.multi_select_rects = []
        self.multi_select_rects = []
        self.multi_select_values = []
        self.multi_sub_rect = None
        self.new_program = []
        self.open_selector = None
        self.play_rect = None
        self.playing = False
        self.position = (0,0)
        self.program = []
        self.rects = []
        self.runner_init_kwargs = kwargs
        self.running = False
        self.screen = screen
        self.scroll = 0
        self.selected = None
        self.selected_anchor = None
        self.time_since_last_run = 0
        self.usable_blocks = usable_blocks
        self.won = False
        self.prevProgramCounter = 0
    def init_block(self,block):
        return block(*block.default_args, **block.default_kwargs)
    def insert_block(self, block, rect):
        rect = pygame.Rect(rect)
        mouse_pos = pygame.mouse.get_pos()
        blocks_to_add = []

        for i in block.blocks_added_before:
            blocks_to_add.append(self.init_block(i))

        blocks_to_add.append(self.init_block(block))

        for i in block.blocks_added_after:
            blocks_to_add.append(self.init_block(i))

        self.program.extend(blocks_to_add)
        self.selected = len(self.program)-len(blocks_to_add)
        self.selected_anchor = (mouse_pos[0]-rect.x,mouse_pos[1]-rect.y)
    def tick(self,events):
        time_passed = self.clock.tick()
        if self.playing:
            self.time_since_last_run += time_passed
            if self.time_since_last_run > 1000:
                self.time_since_last_run = 0
                self.tick_runner(tickCount=True)
        for event in events: 
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.open_selector == None:
                    if event.button == 1:
                        skip = False
                        if self.play_rect is not None and self.play_rect.collidepoint(mouse_pos):
                            self.playing = not self.playing
                            self.init_runner(**self.runner_init_kwargs)
                            skip = True
                        if skip:
                            continue
                        for n,i in enumerate(self.multi_select_rects):
                            if i.collidepoint(event.pos):
                                self.open_selector = n
                                skip = True
                                break
                        if skip:
                            continue
                        for i,rect in enumerate(self.rects): 
                            if rect.collidepoint(mouse_pos) and mouse_pos[1] < self.screen.get_height() - 200: 
                                if self.program[i].endIndent or self.program[i].midIndent:
                                    pass
                                else:
                                    self.selected_anchor = (mouse_pos[0]-rect.x,mouse_pos[1]-rect.y) 
                                    self.selected = i 
                        for rect,block in self.empty_block_rects.items():
                            if pygame.Rect(rect).collidepoint(mouse_pos):
                                self.insert_block(block,rect)
                    if event.button == 4:
                        self.scroll = max(0,self.scroll-50)
                    if event.button == 5:
                        self.scroll = min(self.height-(self.screen.get_height()-200),self.scroll+50)
                else:
                    close = True
                    if self.multi_add_rect and self.multi_add_rect.collidepoint(mouse_pos):
                        self.multi_int_val += 1
                        self.multi_int_val = max(min(self.multi_int_val,self.multi_max_val -1),self.multi_min_val)
                        close = False
                    if self.multi_sub_rect and self.multi_sub_rect.collidepoint(mouse_pos):
                        self.multi_int_val -= 1
                        self.multi_int_val = max(min(self.multi_int_val,self.multi_max_val -1),self.multi_min_val)
                        close = False
                    for v,i in enumerate(self.multi_select_rects):
                        if i.collidepoint(event.pos):
                            if self.multi_select_values[v] == "number" or self.multi_select_values[v] == "address" or self.multi_select_values[v] == "pint":
                                self.multi_select_values[v] = self.multi_int_val
                            self.multi_select_block.setMultiSelect(self.multi_select_index, self.multi_select_values[v])
                            break
                    if close:
                        self.open_selector = None
            if event.type == pygame.MOUSEBUTTONUP:
                
                if event.button == 1 and self.selected != None:

                    if mouse_pos[1] >= self.screen.get_height() - 200:
                        mouse_pos = pygame.mouse.get_pos()
                        startIndex, endIndex = self.get_indexes(mouse_pos)
                        self.program = self.new_program
                        del self.program[startIndex:endIndex]
                        to_delete = []
                        for i,block in enumerate(self.program):
                            if hasattr(block,"jump_id"):
                                found = False
                                for j,b in enumerate(self.program):
                                    if j == i:
                                        continue
                                    if hasattr(b,"jump_id") and b.jump_id == block.jump_id:
                                        found = True
                                if not found:
                                    to_delete.append(i)
                        for i in to_delete:
                            del self.program[i]
                    else:
                        self.program = self.new_program
                    self.selected = None
        game = self.render_game(self.screen.get_width() - 600, self.screen.get_height() - 200)
        self.screen.blit(game, (600,0))
        self.render_program() 
        pygame.draw.rect(self.screen, (128,128,128), (0,self.screen.get_height()-200,self.screen.get_width(),200))
        self.render_empty_blocks((100,self.screen.get_height()-200,self.screen.get_width(),200))
        self.draw_play_button((10,self.screen.get_height()-190))
        self.render_program(second_time=True)
        if self.multi_select_args:
            self.render_multi_select(*self.multi_select_args)
        return self.program, self.won
    def render_empty_blocks(self,rect_to_use):
        x,y,w,h = rect_to_use
        current_x = x
        current_y = y
        max_x = x+w
        for i in self.usable_blocks:
            if i.hidden_from_editor:
                continue
            text = self.font.render(i.prefix, True, (0,0,0))
            current_w = text.get_width()
            if current_x + current_w + 10 > max_x:
                current_x = x
                current_y += 45
            pygame.draw.rect(self.screen, i.color, (current_x,current_y,current_w+10,40))
            self.screen.blit(text, (current_x+5,current_y+5))
            self.empty_block_rects[(current_x,current_y,current_w+10,40)] = i
            current_x += current_w + 15
    def render_multi_select(self, position, place, current, color=(255,255,255), render_dropdown = False,block=None,index = None,second_time=False):

        if place == "if_value":
            options = self.get_valid_values() + ["number"]
        elif place == "if_op":
            options = ["==","!=",">","<",">=","<="]
        elif place == "if_end":
            options = ["then","and","or"]
        elif place == "jump":
            options = ["address"]
        elif place == "move":
            options = ["left","right","up","down"]
        elif place == "pint":
            options = ["pint"]
        else:
            raise ValueError(f"invalid place {place}")
        if render_dropdown:
            self.multi_select_rects = []
            self.multi_select_values = []
            y_offset = 0
            for i in options:
                y_offset += 30
                if i == "number" or i == "address" or i == "pint":
                    text = self.font_small.render(str(self.multi_int_val).zfill(2), True, (0,0,0))
                    add = self.font_small.render("+", True, (0,0,0))
                    sub = self.font_small.render("-", True, (0,0,0))
                    if not second_time:
                        pygame.draw.rect(self.screen, color, (position[0],position[1]+y_offset,30+add.get_width()+sub.get_width()+40,30))
                        self.screen.blit(text, (position[0]+10,position[1]+y_offset+5))
                        self.screen.blit(add, (position[0]+20+30,position[1]+y_offset+5))
                        self.screen.blit(sub, (position[0]+30+30+add.get_width(),position[1]+y_offset+5))
                    self.multi_add_rect = pygame.Rect(position[0]+20+30,position[1]+y_offset,add.get_width(),30)
                    self.multi_sub_rect = pygame.Rect(position[0]+30+30+add.get_width(),position[1]+y_offset,sub.get_width(),30)
                    self.multi_select_rects.append(pygame.Rect(position[0],position[1]+y_offset,50,30))
                    self.multi_select_values.append(i)
                    if i == "number":
                        self.multi_max_val = 100
                        self.multi_min_val = 0
                    elif i == "pint":
                        self.multi_max_val = 100
                        self.multi_min_val = 1
                    else:
                        self.multi_min_val = 0
                        self.multi_max_val = len(self.program)
                    self.multi_int_val = max(min(self.multi_int_val,self.multi_max_val -1),self.multi_min_val)
                else:
                    text = self.font_small.render(i, True, (0,0,0))
                    if not second_time:
                        pygame.draw.rect(self.screen, color, (position[0],position[1]+y_offset,text.get_width()+20,30))
                        self.screen.blit(text, (position[0]+10,position[1]+y_offset))
                    self.multi_select_rects.append(pygame.Rect(position[0],position[1]+y_offset,text.get_width()+20,30))
                    self.multi_select_values.append(i)
                    self.multi_add_rect = None
                    self.multi_sub_rect = None

            return
        text = self.font_small.render(str(current), True, (0,0,0))
        if not second_time:
            pygame.draw.rect(self.screen, color, (position[0],position[1],text.get_width()+20,30))
            self.screen.blit(text, (position[0]+10,position[1]))
        if self.open_selector is not None:
            if len(self.multi_select_rects) == self.open_selector:
                self.multi_select_args = (position,place,current,color,True)
                self.multi_select_block = block
                self.multi_select_index = index
                
        self.multi_select_rects.append(pygame.Rect(position[0],position[1],text.get_width()+20,30))
    def get_multi_select_width(self,current):

        text = self.font_small.render(str(current), True, (0,0,0))
        return text.get_width()+20
    def render_block_label(self, position, label,block, color=(255,255,255),second_time=False):
        x_pos = 0
        for i in label:
            if type(i) == BlockLabelText:
                text = self.font.render(i.text, True, (0,0,0))
                if not second_time:
                    self.screen.blit(text, (position[0]+x_pos,position[1]))
                x_pos += text.get_width()+10
            if type(i) == BlockLabelMultiSelect:
                self.render_multi_select((position[0]+x_pos,position[1]), i.place, block.multiSelect[i.index],color,block=block, index = i.index, second_time = second_time)
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
    def draw_play_button(self, position):
        if not self.playing:
            pygame.draw.rect(self.screen, (0,255,0), (position[0],position[1],50,50))
            pygame.draw.polygon(self.screen, (0,0,0), ((position[0]+15,position[1]+10),(position[0]+15,position[1]+40),(position[0]+35,position[1]+25)))
        else:
            pygame.draw.rect(self.screen, (255,0,0), (position[0],position[1],50,50))
            pygame.draw.line(self.screen, (0,0,0), (position[0]+15,position[1]+10), (position[0]+15,position[1]+40), 10)
            pygame.draw.line(self.screen, (0,0,0), (position[0]+35,position[1]+10), (position[0]+35,position[1]+40), 10)
        self.play_rect = pygame.Rect(position[0],position[1],50,50)
    def move_program(self):
        if self.selected is not None:
            newIndex = self.get_height_of_y_pos(mouse_pos[1] - self.position[1])
            if self.program[startIndex].startIndent: 
                
                indent = 1
                while indent:
                    if endIndex >= len(self.program):
                        break
                    if self.program[endIndex].startIndent:
                        indent += 1
                    elif self.program[endIndex].endIndent:
                        indent -= 1
                    endIndex += 1
                
                if newIndex - startIndex + endIndex > len(self.program): 
                    
                    newIndex = len(self.program) - (endIndex - startIndex)
            self.new_program = self.program.copy() 
            selected_block = self.new_program[startIndex:endIndex] 
            self.new_program = self.new_program[:startIndex] + self.new_program[endIndex:] 
            self.new_program[newIndex:newIndex] = selected_block 
            startIndex, endIndex = newIndex, newIndex + (endIndex-startIndex)
        else:
            self.new_program = self.program.copy()
    def render_block(self, position, block,width, indentLevel, selectIndentLevel, offset, x_offset, is_sub_if = False, is_first_if = True, second_time = False, indentColors = [], highlighted = False):
        if block.midIndent:
            position = (position[0]-20,position[1])
            x_offset = x_offset - 20
        if not is_sub_if and block.prefix == "if":
            temp_offset = 0
            first = True
            for subBlock in block.blockList:
                temp_width = self.get_block_label_width(subBlock.toShowOnBlock(),subBlock)
                self.render_block((position[0], position[1]+temp_offset), subBlock,temp_width, indentLevel, selectIndentLevel, offset+temp_offset, x_offset, is_sub_if = True, is_first_if=first,second_time=second_time)
                first = False
                temp_offset += 40
            return
        w = max(block.minWidth,width+40)
        if block.width is not None:
            w = block.width
        if w is 0:
            second_time = True
        if is_first_if:
            self.end_of_blocks.append((position[0]+w,position[1]+20))
            self.rects.append(pygame.Rect(position[0],position[1],max(width,block.minWidth),40))
        x,y = self.position
        y = y - self.scroll
        if not second_time:
            if highlighted:
                pygame.draw.rect(self.screen, (255,255,0), (position[0]-5,position[1]-5,w+10,50))
            pygame.draw.rect(self.screen, block.color, (position[0],position[1],w,40))
        if block.startIndent:
            if not second_time:
                pygame.draw.rect(self.screen, block.color, (position[0],position[1],10,50))
        self.render_block_label((position[0]+25,position[1]+5),block.toShowOnBlock(),block,saturateRGB(block.color,1.5),second_time=second_time)
        for i in range(indentLevel): 
            if not second_time:
                if i < selectIndentLevel:
                    pygame.draw.rect(self.screen, indentColors[i], (x+i*20,y+offset-10,10,60)) 
                else:
                    pygame.draw.rect(self.screen, indentColors[i], (position[0]-x_offset+(i-selectIndentLevel)*20,position[1]-10,10,60))
    def get_height_of_y_pos(self, y_pos):
        current_height = 0
        index = 0
        for block in self.program:
            if current_height + block.height/2 > y_pos:
                return index
            current_height += block.height
            index += 1
        return index - 1
    def move_program(self, startIndex, newIndex, endIndex):
        self.new_program = self.program.copy() 
        selected_block = self.new_program[startIndex:endIndex] 
        self.new_program = self.new_program[:startIndex] + self.new_program[endIndex:] 
        self.new_program[newIndex:newIndex] = selected_block 
        startIndex, endIndex = newIndex, newIndex + (endIndex-startIndex)
        return startIndex, endIndex
    def get_indexes(self, mouse_pos):
        startIndex = self.selected
        endIndex = self.selected + 1 if self.selected is not None else None
        if self.selected is not None:
            newIndex = self.get_height_of_y_pos(mouse_pos[1] - self.position[1])
            if self.program[startIndex].startIndent: 
                indent = 1
                while indent:
                    if endIndex >= len(self.program):
                        break
                    if self.program[endIndex].startIndent:
                        indent += 1
                    elif self.program[endIndex].endIndent:
                        indent -= 1
                    endIndex += 1
                if newIndex - startIndex + endIndex > len(self.program): 
                    newIndex = len(self.program) - (endIndex - startIndex)
            startIndex, endIndex = self.move_program(startIndex, newIndex, endIndex)
        else:
            self.new_program = self.program.copy() 
        return startIndex, endIndex
    def render_program(self,second_time = False):
        self.multi_select_args = None
        x,y = self.position 
        y = y - self.scroll
        offset = 0
        indentLevel = 0
        selectIndentLevel = 0
        selectOffset = 0
        self.end_of_blocks = []
        indentColor = (150,150,0) 
        mouse_pos = pygame.mouse.get_pos()
        renderOpenMultiSelectArgs = []
        startIndex, endIndex = self.get_indexes(mouse_pos)
        self.multi_select_rects = []
        self.rects = [] 
        indentColors = []
        for i,block in enumerate(self.new_program): 
            width = self.get_block_label_width(block.toShowOnBlock(),block)
            if block.endIndent:
                indentLevel -= 1
                indentColors.pop()
            x_offset = indentLevel*20 
            if i == startIndex: 
                selectOffset = - offset 
                selectIndentLevel = indentLevel
            highlighted = i == self.prevProgramCounter
            if startIndex is not None and i >= startIndex and i < endIndex: 
                x_offset = (indentLevel-selectIndentLevel)*20 
                self.render_block((mouse_pos[0] - self.selected_anchor[0] + x_offset,mouse_pos[1] - self.selected_anchor[1] + offset + selectOffset), block, width,indentLevel,selectIndentLevel, offset, x_offset,indentColors = indentColors,highlighted=highlighted)
            else:
                self.render_block((x+x_offset,y+offset), block, width,indentLevel, indentLevel, offset, 0,second_time=second_time,indentColors = indentColors,highlighted=highlighted)
            offset += block.height 
            if block.startIndent: 
                indentLevel += 1
                indentColors.append(block.color)
        self.height = offset 
        random.seed(5)
        x_pos = 400
        for i,block in enumerate(self.new_program):
            if block.prefix == "jump":
                for j,b in enumerate(self.new_program):
                    if isinstance(b, blocks.jumpToBlock) and hasattr(b,"jump_id") and b.jump_id == block.jump_id:
                        draw_arrow(screen, self.end_of_blocks[i], self.end_of_blocks[j], x_pos, color = randomRGB(seed=block.jump_id))
                        x_pos += 20
    def tick_runner(self, tickCount = False):
        self.last_move = None
        if self.check_win():
            self.playing = False
            self.won = True
            return True
        if self.programCounter == len(self.program):
            self.playing = False
        self.timesRunCurrent += 1
        if len(self.program) <= self.programCounter:
            return True
        self.prevProgramCounter = self.programCounter
        result_of_run = self.program[self.programCounter].run(self)
        if result_of_run:
            self.prevProgramCounter = self.programCounter
            self.programCounter += 1
            self.timesRunCurrent = 0
        if tickCount:
            self.ticks_passed += 1
        return False
    # functions that each type of level will override
    def init_runner(self, **kwargs):
        # Used to store world states from the level data
        self.world = kwargs
    def render_game(self,w,h):
        game = pygame.Surface((w,h))
        game.fill((255,0,0))
        return game
    def value_getter(self, valueToGet):
        if type(valueToGet) == int:
            return valueToGet
        if valueToGet == "player_x":
            return self.world["player_x"]
        if valueToGet == "player_y":
            return self.world["player_y"]
    def validate_value_getter(self, valueToTest):
        if valueToTest == "player_x" or valueToTest == "player_y":
            return True
        return False
    def get_valid_values(self):
        return ["player_x","player_y"]
    def check_win(self):
        return False