import random

class Bot:
    def __init__(self,
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                ):

        self.width = width
        self.height = height
        self.agents = agents

    def compute_action(self, state):
        raise NotImplementedError


class MinMaxBot(Bot):
    def compute_action(self, state):
        pass

class RandomBot(Bot):
    def compute_action(self, state):
        agent = state["turn"]
        actions = {agent: [(random.randint(0, self.width-1), random.randint(0, self.height-1))]}
        # print(f"actions: {actions}")
        return actions

class CycleBot(Bot):
    def __init__(self, *args, **kwargs):
        super(CycleBot, self).__init__(*args, **kwargs)
        self.steps = 0

    def compute_action(self, state):
        actions = {}
        center = (self.width//2, self.height//2)
        if(self.steps == 0):
            small_box, big_box = 2, 4
            actions = {self.agents[0]:[], self.agents[1]:[]}
            for i in range(center[0]-small_box, center[0]+small_box):
                actions[self.agents[0]].append([i, center[1]-small_box])
            for i in range(center[0]-small_box, center[0]+small_box):
                actions[self.agents[0]].append([i, center[1]+small_box])
            for i in range(center[1]-small_box, center[1]+small_box):
                actions[self.agents[0]].append([center[0]-small_box, i])
            for i in range(center[1]-small_box, center[1]+small_box+1):
                actions[self.agents[0]].append([center[0]+small_box, i])

            for i in range(center[0]-big_box, center[0]+big_box):
                actions[self.agents[1]].append([i, center[1]-big_box])
            for i in range(center[0]-big_box, center[0]+big_box):
                actions[self.agents[1]].append([i, center[1]+big_box])
            for i in range(center[1]-big_box, center[1]+big_box):
                actions[self.agents[1]].append([center[0]-big_box, i])
            for i in range(center[1]-big_box, center[1]+big_box+1):
                actions[self.agents[1]].append([center[0]+big_box, i])
        self.steps += 1
        return actions