def goal(renderer, data):
    if renderer.player_x == renderer.goal_x and renderer.player_y == renderer.goal_y:
        return True
    return False
def box_at_pos(renderer, data):
    for item in renderer.items:
        if item["x"] == data["x"] and item["y"] == data["y"]:
            return True
    return False


win_conditions = {}
for func in list(globals().values()):
    if callable(func):
        win_conditions[func.__name__.replace("_","-")] = func