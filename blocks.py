from blockMaker import *
from if_blocks import *
import time
import operator
import itertools

#example block
"""
@blockWrapper
def exampleBlock(blockList):
    startIndent = False # used for if blocks and loops
    endIndent = False # used for the end of if blocks and loops
    prefix = "example" # used for converting text to code, to know which block to use
    color = (0,0,0) # color of the block. black shouldn't be used as the text is also black
    def __init__(self, number):
        #init should perform type checks and raise errors.
        typeCheck(number, int)
        #init should also set parameters to attributes
        self.number = number
    def run(self, runner):
        #what code to run.
        #runner is a runner class defined in runner.py
        #see runner.py for what you could call.
        print(self.number)
        #should return true or false.
        #if true, the runner will continue to the next block
        #if false, the runner will run this block again next tick
        
        #this function should not always return false, as it would cause an infinite loop.
        # unless you change runner.programCounter to a different value
        return True
    def toText(self):
        # used when printing in console, and displayed inside the block.
        return "example " + str(self.number)
    def fromText(text):
        # used when parsing from clipboard.
        # should turn text into an instance of this.
        # should be the inverse of toText but this may change to another function in the future
        return exampleBlock(int(text[8:]))
"""

@blockWrapper
class repeatBlock(Block):
    startIndent = True
    endIndent = False
    prefix = "repeat"
    color = (0,128,128)
    default_args = ["1"]
    def __init__(self, repeat_amount):
        repeat_amount = typeCheck(repeat_amount, int, ParserError, "Wait time must be an integer")
        self.repeat_amount = repeat_amount
        self.repeated = 0
        self.multiSelect = [repeat_amount]
    def run(self, runner):
        self.repeated = 0
        return True
    def toText(self):
        return "repeat " + str(self.repeat_amount)
    def fromText(text):
        return waitBlock(text[5:])
    def validateValues(self):
        return True
    def toShowOnBlock(self):
        return [BlockLabelText("repeat "), BlockLabelMultiSelect("pint", 0)]
    def setMultiSelect(self, index, value):
        if index == 0:
            self.repeat_amount = value
        self.multiSelect[index] = value
@blockWrapper
class endRepeatBlock(Block):
    startIndent = False
    endIndent = True
    prefix = "endrepeat"
    color = (0,128,128)
    height = 10
    minWidth = 0
    width = 0
    size = 0
    def run(self, runner):
        position = runner.programCounter
        indent = 1
        while indent > 0:
            position -= 1
            if 0 > position:
                break
            block = runner.program[position]
            if block.endIndent:
                indent += 1
            elif block.startIndent:
                indent -= 1
        block.repeated += 1
        print(block.repeated, block.repeat_amount, position)
        if block.repeated >= block.repeat_amount:
            runner.programCounter += 1
            runner.tick_runner()
            return False
        runner.programCounter = position
        return True
    def toText(self):
        return ""
    def fromText(text):
        return waitBlock(text[5:])
    def validateValues(self):
        return True
@blockWrapper
class moveBlock(Block):
    prefix = "move"
    color = (150,150,0)
    default_args =["right"]
    def __init__(self, movement_direction):
        self.movement_direction =movement_direction
        self.multiSelect = [self.movement_direction]
    def setMultiSelect(self, index, value):
        self.movement_direction = value
        self.multiSelect[index] = value
    def run(self, runner):
        runner.move(self.movement_direction)
        return True
    def toText(self):
        return "move " + str(self.movement_direction)
    def fromText(text):
        return moveBlock(text[5:])
    def toShowOnBlock(self):
        return [BlockLabelText("move "),BlockLabelMultiSelect("move",0)]
    def validateValues(self):
        return self.movement_direction in ["left","right","up","down"]
def jumpIdGenerator():
    for i in itertools.count():
        yield i
        yield i # yield twice, once for jump and once for jumpTo

jumpIdGenerator = jumpIdGenerator()

@blockWrapper
class jumpBlock(Block):
    prefix = "jump"
    startIndent = False
    endIndent = False
    color = (150,150,0)
    def __init__(self):
        self.jump_id = next(jumpIdGenerator)
    def run(self, runner):
        for i,block in enumerate(runner.program):
            if isinstance(block, jumpToBlock) and block.jump_id == self.jump_id:
                runner.programCounter = i
        # set program counter
        return False
    def toText(self):
        return "jump "
    def fromText(text):
        return jumpBlock(text[5:])
    def validateValues(self):
        return type(jump_id) == int
@blockWrapper
class jumpToBlock(Block):
    prefix = "jumpto"
    startIndent = False
    endIndent = False
    minWidth = 80
    color = (150,150,0)
    def __init__(self):
        self.jump_id = next(jumpIdGenerator)
    def run(self, runner):
        runner.programCounter += 1 # go to next instruction
        runner.tick_runner()
        return False
    def toText(self):
        return ""
    def fromText(text):
        return jumpToBlock(text[5:])
    def validateValues(self):
        return type(jump_id) == int

jumpBlock.blocks_added_after = [jumpToBlock]
repeatBlock.blocks_added_after = [endRepeatBlock]