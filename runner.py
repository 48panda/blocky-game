import time
import blocks
class Runner:
    def __init__(self, program,world):
        self.world = world
        self.program = program
        self.timesRunCurrent = 0
        self.programCounter = 0
    def tick(self):
        self.timesRunCurrent += 1
        if len(self.program) <= self.programCounter:
            return True
        result_of_run = self.program[self.programCounter].run(self)
        if result_of_run:
            self.programCounter += 1
            self.timesRunCurrent = 0
        if len(self.program) <= self.programCounter:
            return True
        return False
    def valueGetter(self, valueToGet):
        if type(valueToGet) == int:
            return valueToGet
        if valueToGet == "player_x":
            return self.world.player_x
        if valueToGet == "player_y":
            return self.world.player_y
    def validateValueGetter(self, valueToTest):
        if valueToTest == "player_x" or valueToTest == "player_y":
            return True
        return False
    def PerformAction(self,action):
        if action == "move_left":
            self.world.player_x -= 1
        elif action == "move_right":
            self.world.player_x += 1
        elif action == "move_up":
            self.world.player_y -= 1
        elif action == "move_down":
            self.world.player_y += 1
        else:
            raise ParserError("Invalid action")
    def get_valid_values(self):
        return ["player_x","player_y"]