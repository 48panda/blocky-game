from blockMaker import *
import time
import operator
blockList = []
blockWrapper = getBlockWrapper(blockList) # get block wrapper

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

# if blocks
@blockWrapper
class ifBlock(Block):
    prefix = "if"
    startIndent = True
    endIndent = False
    color = (150,150,0)
    def __init__(self, condition):
        #set condition, needed for toText
        self.condition = condition
        ops = {"==":operator.eq, "!=":operator.ne, ">":operator.gt, "<":operator.lt, ">=":operator.ge, "<=":operator.le}
        condition = condition.split(" ")
        if len(condition) != 3: # validate condition structure
            raise ParserError("If statement must have 3 parts")
        if condition[1] not in ops: # validate operator
            raise ParserError("If statement must have a valid operator")
        try:
            self.left_side = int(condition[0]) # values can be ints but may not be.
        except:
            self.left_side = condition[0]
        self.operator = condition[1] # get operator
        try:
            self.right_side = int(condition[2]) # values can be ints but may not be.
        except:
            self.right_side = condition[2]
        self.multiSelect = [self.left_side,self.operator,self.right_side]
    def setMultiSelect(self, index, value):
        if index == 0:
            self.left_side = value
        elif index == 1:
            self.operator = value
        elif index == 2:
            self.right_side = value
        self.multiSelect[index] = value
    def run(self, runner):
        ops = {"==":operator.eq, "!=":operator.ne, ">":operator.gt, "<":operator.lt, ">=":operator.ge, "<=":operator.le}
        if type(self.left_side) != int and (not runner.validateValueGetter(self.left_side)):
            raise ParserError("If statement must have valid values") # this depends on the environment, so it must be done at runtime.
            # Luckily, this is only caused if the user messes with the code or pastes into different environments.
        if type(self.right_side) != int and (not runner.validateValueGetter(self.right_side)):
            raise ParserError("If statement must have valid values")
        if ops[self.operator](runner.valueGetter(self.left_side), runner.valueGetter(self.right_side)): # if the condition is true, run the code inside the if \
            # (happens to be the next line of code)
            return True
        # if not true, run the next line of code after the corresponding endif
        block = runner.program[runner.programCounter]
        indent = 1
        while indent > 0: # when indent is 0, we are at the endif that closes this if
            runner.programCounter += 1
            if len(runner.program) <= runner.programCounter:
                break
            block = runner.program[runner.programCounter]
            if block.startIndent:
                indent += 1
            elif block.endIndent:
                indent -= 1
        return False
    def toText(self):
        return "if  " + str(self.condition)
    def fromText(text):
        return ifBlock(text[3:])
    def toShowOnBlock(self):
        return [BlockLabelText("if "),BlockLabelMultiSelect("if_value",0),BlockLabelMultiSelect("if_op",1),BlockLabelMultiSelect("if_value",2)]

@blockWrapper
class endifBlock(Block): # block for the end of an if
    prefix = "endif"
    startIndent = False
    endIndent = True
    color = (150,150,0)
    def __init__(self):
        pass
    def run(self, runner):
        runner.programCounter += 1
        runner.tick() # endif block shouldn't take any ticks so we increment program counter and tick
        # i don't know of any side effects of this, but i'm sure there is one.
        return False
    def toText(self):
        return "endif"
    def fromText(text):
        return endifBlock()
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