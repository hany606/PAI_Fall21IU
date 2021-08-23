import random
from copy import deepcopy
import numpy as np

class Node:
    def __init__(self, parent=None, children=None, value=None, action=None, best_child=None):
        self.parent = parent
        self.children = children
        self.value = value
        self.action = action
        self.best_child = best_child

    def __repr__(self):
        return f"Children num.: {len(self.children)}, value: {self.value}, action: {self.action}"

class Bot:
    def __init__(self,
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                ):

        self.width = width
        self.height = height
        self.agents = agents

    def compute_action(self, state, prev_action=None):
        raise NotImplementedError

    def plan(self, env):
        print("plan() function is useless for this bot")

class MinMaxBot(Bot):
    max_val = 9999999999
    root = Node(parent=None, children=[], value=-max_val, action=None, best_child=None)
    def __init__(self, 
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                 max_val=max_val,
                 root=root):
        super(MinMaxBot, self).__init__(width=width, height=height, agents=agents)
        self.max_val = max_val
        self.min_val = -self.max_val
        self.root = root
        self.search_node = self.root

    # Note: agent_turn is 1-indexed
    # For planning then execution manner
    def compute_action_old(self, state, prev_action, agent_turn=2):
        agent_turn -= 1
        children = self.root.children
        for c in children:
            # Fetch which node/action that the user selected
            if(prev_action == c.action):
                best_child = c.best_child
                action = {self.agents[agent_turn]: [best_child.action]}
                return action
        raise Exception('Did not find a child ??!')

    # For online manner
    def compute_action(self, env, prev_action=None, agent_turn=2, depth=0, max_depth=3, max_width=10, random_explore=False):
        agent_turn -= 1
        action = {self.agents[agent_turn]: [self.compute(env, depth, max_depth, max_width, random_explore)]}
        return action
    # ------------------------------------------------------------------------------------
    # For testing only: Based on: https://cs50.harvard.edu/ai/2020/notes/0/, https://github.com/wbsth/cs50ai/blob/master/week0/tictactoe/tictactoe.py
    def _result(self, env_, action_):
        env_copy = deepcopy(env_)
        # print(env_copy.get_turn())
        action_step = {env_copy.get_turn():[action_]}
        _ = env_copy.step(action_step)
        return env_copy

    def _max_value(self, env_,depth, max_depth=3, max_width=10, random_explore=False):
        # print(max_depth, max_width, random_explore)
        optimal_action = ()
        if env_.get_done() or depth > max_depth:
            scores = env_.get_scores()
            score = scores[self.agents[0]] - scores[self.agents[1]]  # if the blue agent is more, then it is positive, if the red agent is more then it is negative
            return score, optimal_action
        value = self.min_val

        action_set_idx = None
        if(random_explore):
            action_set_idx = np.random.choice(len(env_.get_possible_actions()), min(max_width, len(env_.get_possible_actions())), replace=False)
        else:
            action_set_idx = [i for i in range(min(max_width, len(env_.get_possible_actions())))]
        # for i in range(min(max_width, len(env_.get_possible_actions()))):
        for i in action_set_idx:
            action = env_.get_possible_actions()[i]
            min_value = self._min_value(self._result(env_,action),depth+1, max_depth, max_width, random_explore)[0]
            if min_value > value:
                value = min_value
                optimal_action = action
        return value, optimal_action

    def _min_value(self, env_,depth, max_depth=3, max_width=10, random_explore=False):
        # print(max_depth, max_width, random_explore)
        optimal_action = ()
        if env_.get_done() or depth > max_depth:
            scores = env_.get_scores()
            score = scores[self.agents[0]] - scores[self.agents[1]]  # if the blue agent is more, then it is positive, if the red agent is more then it is negative
            return score, optimal_action
        value = self.max_val

        action_set_idx = None
        if(random_explore):
            action_set_idx = np.random.choice(len(env_.get_possible_actions()), min(max_width, len(env_.get_possible_actions())), replace=False)
        else:
            action_set_idx = [i for i in range(min(max_width, len(env_.get_possible_actions())))]
        # for i in range(min(max_width, len(env_.get_possible_actions()))):
        for i in action_set_idx:
            action = env_.get_possible_actions()[i]
            max_value = self._max_value(self._result(env_,action),depth+1, max_depth, max_width, random_explore)[0]
            if max_value < value:
                value = max_value
                optimal_action = action
        return value, optimal_action

    # This works in online manner
    def compute(self, env, depth=0, max_depth=3, max_width=10, random_explore=False):
        if env.get_done():
            return None

        if(env.get_turn() == self.agents[0]): # maximizer
            print("Maximizer")
            return self._max_value(env, depth+1, max_depth, max_width, random_explore)[1]

        elif(env.get_turn() == self.agents[1]): # minimizer
            print("Minimizer")
            return self._min_value(env, depth+1, max_depth, max_width, random_explore)[1]
    # ------------------------------------------------------------------------------------
    
    def plan(self, env):
        env.reset()
        self.minimax(env)
    
    def minimax(self, env, parent=root, depth=0):
        print(depth)
        # env.render(timeout=0.000001)

        # print(parent)
        # print(env.state_matrix)
        candidate_solutions = env.get_possible_actions()
        # print(depth, len(candidate_solutions))

        # print(candidate_solutions)
        if(len(candidate_solutions) == 0 or env.get_done()): # end of the game
            scores = env.get_scores()
            score = scores[self.agents[0]] - scores[self.agents[1]]  # if the blue agent is more, then it is positive, if the red agent is more then it is negative
            parent.value = score
            # print("leaf")
            return parent#score

        # if(env.get_turn() == self.agents[0]): # maximizer
        #     parent.value = self.min_val
        # elif(env.get_turn() == self.agents[1]): # minimizer
        #     parent.value = self.max_val
        # print("------------- Loop on candidates --------------")
        # # For each child from the candidate solutions
        # for i,c in enumerate(candidate_solutions):
        #     # Take step for that solution
        #     action = {env.get_turn(): [c]}
        #     # action = {self.agents[depth%2]: [c]}
        #     print(env.get_turn())
        #     # print(action)
        #     env = deepcopy(env)
        #     obs, res, done, info = env.step(action)
        #     # print(obs)
        #     # exit()
        #     child_node = Node(parent=parent, children=[], value=None, action=c, best_child=None)
        #     parent.children.append(child_node)
        #     # print(env.get_turn(), self.agents)
        #     print(f"Before: {env.num_steps}")
        #     print(f"{i}/{len(candidate_solutions)}")
        #     print(candidate_solutions, c)
        #     print("#################")
        #     # print(env.state_matrix)
        #     score = self.minimax(env, parent=child_node, depth=depth+1)
        #     print(f"After: {env.num_steps}")
        #     print(f"{i}/{len(candidate_solutions)}")
        #     print(candidate_solutions, c)
        #     print("#################")
        #     env.render(timeout=-0.00001)

        #     # print("After")
        #     # print(env.state_matrix)
        #     # print(depth)
        #     # print(parent.value, score)
        #     # print(env.get_turn(), self.agents, score)

        #     if(env.get_turn() == self.agents[0]): # maximizer
        #     # if(depth%2 == 0):
        #         # Get the maximum from the children
        #         # parent.value = max(parent.value, score)
        #         if(parent.value <= score):
        #             parent.value = score
        #             parent.best_child = child_node
        #     elif(env.get_turn() == self.agents[1]): # minimizer
        #     # else:
        #         # Get the minimum from the children
        #         # parent.value = min(parent.value, score)
        #         if(parent.value >= score):
        #             parent.value = score
        #             parent.best_child = child_node
        # print("------------- Finished candidates --------------")
        # return parent.value

        # Return the node value after being selected

        # if(env.get_turn() == self.agents[0]): # maximizer
        if(depth%2 == 0):
            # For each child from the candidate solutions
            parent.value = self.min_val
            for c in candidate_solutions:
                # Take step for that solution
                # print(c, "Max-blue")
                action = {self.agents[0]: [c]}
                env_copy = deepcopy(env)
                _ = env_copy.step(action)
                # env_copy.render(timeout=-0.00001)
                child_node = Node(parent=parent, children=[], value=None, action=c)
                parent.children.append(child_node)
                returned_parent = self.minimax(env_copy, parent=child_node, depth=depth+1)
                score = returned_parent.value
                # Get the maximum from the children
                # parent.value = max(parent.value, score)
                # print("Max")
                if(parent.value <= score):
                    parent.value = score
                    parent.best_child = child_node
            # print(f"Max-blue: out of {parent.action}")
        # elif(env.get_turn() == self.agents[1]): # minimizer
        else:
            # For each child from the candidate solutions
            parent.value = self.max_val
            for c in candidate_solutions:
                # print(c, "Min-Red")
                # Take step for that solution
                action = {self.agents[1]: [c]}
                env_copy = deepcopy(env)
                _ = env_copy.step(action)
                # env_copy.render(timeout=-0.00001)
                child_node = Node(parent=parent, children=[], value=None, action=c)
                parent.children.append(child_node)
                returned_parent = self.minimax(env_copy, parent=child_node, depth=depth+1)
                score = returned_parent.value
                # Get the minimum from the children
                # parent.value = min(parent.value, score)
                # print("Min")
                if(parent.value >= score):
                    parent.value = score
                    parent.best_child = child_node
            # print(f"Min-red: out of {parent.action}")
        return parent

class RandomBot(Bot):
    def compute_action(self, state, prev_action=None):
        agent = state["turn"]
        actions = {agent: [(random.randint(0, self.width-1), random.randint(0, self.height-1))]}
        # print(f"actions: {actions}")
        return actions

class CycleBot(Bot):
    def __init__(self, *args, **kwargs):
        super(CycleBot, self).__init__(*args, **kwargs)
        self.steps = 0

    def compute_action(self, state, prev_action=None):
        actions = {}
        center = (self.width//2, self.height//2)
        if(self.steps == 0):
            small_box, big_box = 3, 4
            # actions = {self.agents[1]:[], self.agents[0]:[]}
            # actions[self.agents[1]].append(center)

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