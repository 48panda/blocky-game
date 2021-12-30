from blockMaker import *
from if_blocks import *
import time
import operator

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
class waitBlock(Block):
    startIndent = False
    endIndent = False
    prefix = "wait"
    color = (0,255,255)
    default_args = ["0"]
    def __init__(self, time):
        time = typeCheck(time, int, ParserError, "Wait time must be an integer")
        self.time = time
    def run(self, runner):
        return runner.timesRunCurrent >= self.time
        #waits time ticks before returning true
    def toText(self):
        return "wait " + str(self.time)
    def fromText(text):
        return waitBlock(text[5:])

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

@blockWrapper
class jumpBlock(Block):
    prefix = "jump"
    startIndent = False
    endIndent = False
    color = (150,150,0)
    default_args =["0"]
    def __init__(self, jump_loc):
        jump_loc = typeCheck(jump_loc, int, ParserError, "Jump location must be an integer")
        self.jump_loc = jump_loc
        self.multiSelect = [self.jump_loc]
    def setMultiSelect(self, index, value):
        self.jump_loc = value
        self.multiSelect[index] = value
    def run(self, runner):
        runner.programCounter = self.jump_loc
        # set program counter
        return False
    def toText(self):
        return "jump " + str(self.jump_loc)
    def fromText(text):
        return jumpBlock(text[5:])
    def toShowOnBlock(self):
        return [BlockLabelText("jump "),BlockLabelMultiSelect("jump",0)]