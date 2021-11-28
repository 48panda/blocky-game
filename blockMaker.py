def getBlockWrapper(blockList):
    # makes a wrapper that adds the block to the blockList
    def blockWrapper(block):
        blockList.append(block)
        return block
    return blockWrapper
class Block:
    # base class for blocks
    def __str__(self):#in case we want to change the string method later
        return self.toText()
    __repr__ = __str__ # repr is string for now because list stringify uses repr

class ParserError(Exception):pass # exception we can catch to find invalid text input (will not cause error but show error on screen)

def typeCheck(arg,type,errorType,errorMessage):
    # arg is always a string, so this function checks if you can cast it to the right type.
    try:
        return type(arg)
    except:pass # raise outside of try block to avoid polluting stack with the type cast error as this will not help the user
    raise errorType(errorMessage)