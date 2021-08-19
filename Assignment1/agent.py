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
        actions = {agent: [random.randint(0, self.width-1), random.randint(0, self.height-1)]}
        return actions