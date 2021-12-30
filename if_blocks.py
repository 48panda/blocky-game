#There's a few if blocks so this is to group them into a single file
from blockMaker import *
import operator
ops = {"==":operator.eq, "!=":operator.ne, ">":operator.gt, "<":operator.lt, ">=":operator.ge, "<=":operator.le}
blockList = []
blockWrapper = getBlockWrapper(blockList) # get block wrapper
@blockWrapper
class ifBlock(Block):
    prefix = "if"
    startIndent = True
    endIndent = False
    color = (150,150,0)
    default_args = ["0 == 0 then"]
    def __init__(self, condition):
        self.condition = condition
        self.blockList = []
        condition = self.condition.split(" ")
        conditions = [condition[i:i+4] for i in range(0, len(condition), 4)]
        for condition in conditions:
            self.blockList.append(ifSubBlock(" ".join(condition), self))
        self.blockList[0].isFirst = True
        self.height = len(self.blockList) * 40 + 10
    def run(self, runner):
        wholeBoolean = True
        currentOrSection = False
        for block in self.blockList:
            currentOrSection = currentOrSection or block.get_true_or_false(runner)
            if block.end != "or":
                wholeBoolean = wholeBoolean and currentOrSection
                currentOrSection = False
        if wholeBoolean:
            return True
        block = runner.program[runner.programCounter]
        indent = 1
        while indent > 0:
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
        return "if " + self.condition
    def fromText(self, text):
        self.condition = text[3:]
    def changeEndValue(self, block, oldValue, newValue):
        if oldValue == newValue:
            return
        if newValue == "then":
            index = self.blockList.index(block)
            self.blockList = self.blockList[:index+1]
        if oldValue == "then":
            self.blockList.append(ifSubBlock("0 == 0 then", self))
        self.height = len(self.blockList) * 40 + 10



# no wrapper, because it is a subblock, only used internally
class ifSubBlock(Block):
    # no prefix needed either
    startIndent = True # indent needed for the small thing for if the block is empty
    color = (150,150,0)
    def __init__(self, condition, parent):
        self.parent = parent
        self.isFirst = False
        self.condition = condition
        condition = condition.split(" ")
        try:
            self.left_side = int(condition[0])
        except:
            self.left_side = condition[0]
        self.operator = condition[1]
        try:
            self.right_side = int(condition[2])
        except:
            self.right_side = condition[2]
        if len(condition) == 4:
            self.end = condition[3]
        else:
            self.end = "then"
        self.multiSelect = [self.left_side,self.operator, self.right_side, self.end]
    def setMultiSelect(self, index, value):
        if index == 0:
            self.left_side = value
        elif index == 1:
            self.operator = value
        elif index == 2:
            self.right_side = value
        elif index == 3:
            self.parent.changeEndValue(self, self.end, value)
            self.end = value
        self.multiSelect[index] = value
    def get_true_or_false(self,runner):
        # TODO: VALIDATION
        left_side = self.left_side
        right_side = self.right_side
        if type(left_side) == str:
            if runner.validate_value_getter(left_side):
                left_side = runner.value_getter(left_side)
        if type(right_side) == str:
            if runner.validate_value_getter(right_side):
                right_side = runner.value_getter(right_side)
        return ops[self.operator](left_side, right_side)
    def toShowOnBlock(self):
        if self.isFirst:
            return [BlockLabelText("if "), BlockLabelMultiSelect("if_value", 0),BlockLabelMultiSelect("if_op", 1), BlockLabelMultiSelect("if_value", 2), BlockLabelMultiSelect("if_end", 3)]
        else:
            return [BlockLabelText("   "), BlockLabelMultiSelect("if_value", 0),BlockLabelMultiSelect("if_op", 1), BlockLabelMultiSelect("if_value", 2), BlockLabelMultiSelect("if_end", 3)]
"""
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
        self.multiSelect = [self.left_side,self.operator,self.right_side,"then"]
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
        if type(self.left_side) != int and (not runner.validate_value_getter(self.left_side)):
            raise ParserError("If statement must have valid values") # this depends on the environment, so it must be done at runtime.
            # Luckily, this is only caused if the user messes with the code or pastes into different environments.
        if type(self.right_side) != int and (not runner.validate_value_getter(self.right_side)):
            raise ParserError("If statement must have valid values")
        if ops[self.operator](runner.value_getter(self.left_side), runner.value_getter(self.right_side)): # if the condition is true, run the code inside the if \
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
        return [BlockLabelText("if "),BlockLabelMultiSelect("if_value",0),BlockLabelMultiSelect("if_op",1),BlockLabelMultiSelect("if_value",2),BlockLabelMultiSelect("if_end",3)]
"""
@blockWrapper
class endifBlock(Block): # block for the end of an if
    prefix = "endif"
    startIndent = False
    endIndent = True
    hidden_from_editor = True
    color = (150,150,0)
    def __init__(self):
        pass
    def run(self, runner):
        runner.programCounter += 1
        runner.tick_runner() # endif block shouldn't take any ticks so we increment program counter and tick
        # i don't know of any side effects of this, but i'm sure there is one.
        return False
    def toText(self):
        return "endif"
    def fromText(text):
        return endifBlock()
@blockWrapper
class elseBlock(Block): # block for the end of an if
    prefix = "else"
    midIndent = True
    color = (150,150,0)
    def __init__(self):
        pass
    def run(self, runner):
        runner.programCounter += 1
        runner.tick_runner() # endif block shouldn't take any ticks so we increment program counter and tick
        # i don't know of any side effects of this, but i'm sure there is one.
        return False
    def toText(self):
        return "else"
    def fromText(text):
        return elseBlock()


ifBlock.blocks_added_after = [endifBlock]
elseBlock.blocks_added_after = [endifBlock]
elseBlock.blocks_added_before = [ifBlock]