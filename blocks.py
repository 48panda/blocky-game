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
    def __init__(self, time):
        typeCheck(time, int, ParserError, "Wait time must be an integer")
        self.time = time
    def run(self, runner):
        return runner.timesRunCurrent >= self.time
        #waits time ticks before returning true
    def toText(self):
        return "wait " + str(self.time)
    def fromText(text):
        return waitBlock(text[5:])

#will be deleted, python console not visible in-game
@blockWrapper
class printBlock(Block):
    prefix = "print"
    startIndent = False
    endIndent = False
    color = (255,0,255)
    def __init__(self, toPrint):
        typeCheck(toPrint, str, ParserError, "Can only print strings")
        self.toPrint = toPrint
    def run(self, runner):
        print(self.toPrint)
        return True
    def toText(self):
        return "print " + str(self.toPrint)
    def fromText(text):
        return printBlock(text[6:])

@blockWrapper
class jumpBlock(Block):
    prefix = "jump"
    startIndent = False
    endIndent = False
    color = (150,150,0)
    def __init__(self, jumpLoc):
        typeCheck(jumpLoc, int, ParserError, "Jump location must be an integer")
        self.jumpLoc = jumpLoc
        self.multiSelect = [self.jumpLoc]
    def setMultiSelect(self, index, value):
        self.jumpLoc = value
        self.multiSelect[index] = value
    def run(self, runner):
        runner.programCounter = self.jumpLoc
        # set program counter
        return False
    def toText(self):
        return "jump " + str(self.jumpLoc)
    def fromText(text):
        return endifBlock(text[5:])
    def toShowOnBlock(self):
        return [BlockLabelText("jump "),BlockLabelMultiSelect("jump",0)]