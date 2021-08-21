import numpy as np
from Network import Network


# Actions: coordinate of the block
# Observation: {"world":state_matrix, "agent_turn"}

class Dots:
    def __init__(self, 
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                 agents_colors={"blue":"blue", "red":"red"},
                 max_num_step=100,
                 node_size=5):
        
        self.width = width
        self.height = height
        self.agents = agents
        self.agents_colors = agents_colors
        self.turn_counter = 0
        self.steps_counter = 0
        self.max_num_step = max_num_step
        self.network = Network(width, height, node_size=node_size)
    
    # Note: Must be called at first
    def reset(self):
        self.state_matrix = np.zeros((self.width, self.height), dtype=str)
        return self.get_observation()

    def render(self, timeout=0.0001):
        self.network.draw(timeout=timeout)
        

    def get_observation(self):
        obs = {"world": self.state_matrix, "turn": self.agents[self.turn_counter]}
        return obs

    def get_reward(self):
        return 0

    # Just for testing 
    def get_done(self):
        if(self.steps_counter >= self.max_num_step):
            return True
        return False

    def get_info(self):
        return {}

    # TODO:
    # Cycle detection algorithm for the graph
    # Add edges to the graph
    def _create_cycles(self):
        pass

    # TODO:
    # Implement a method to detect if the position is inside a cycle (loop over all the occuipied positions)
    #   If it is then change that position to the other agent color
    def _update_cycle(self):
        pass

    def _dist(self, p1, p2):
        dx = (p1[0] - p2[0])
        dy = (p1[1] - p2[1])
        return (dx * dx + dy * dy)**0.5

    def _add_edges(self, agent, point):
        directions = [(-1,-1), (1,1), (-1,1), (1,-1), (0,1), (0,-1), (1,0), (-1,0)]
        for d in directions:
            p = [point[i]+d[i] for i in range(2)]
            # print(self.state_matrix[p[0], p[1]], self.state_matrix[point[0], point[1]], agent)
            if(p[0] >= self.width or p[1] >= self.height or p[0] < 0 or p[1] < 0):
                # print("Out", p, point)
                continue
            if(self.state_matrix[p[0], p[1]] == agent[0]): # because something for numpy array
                self.network.add_edge(point[0], point[1], p[0], p[1], agent, self.agents_colors[agent])
                # print(f"Add edge {point} -> {p}, dist={self._dist(point,p)}")
                # print(f"Ids {self.network.get_id(*point)} -> {self.network.get_id(*p)}")

    def _add_node(self, agent, point):
        self.state_matrix[point[0], point[1]] = agent
        self.network.add_node(point[0], point[1], agent, agent)
        self._add_edges(agent, point)

    def _update_cycle(self, agent, node):
        cycles = self.network.find_cycles(agent, node)
        return len(cycles)

    # Actions is dictionary with key the agent id -> agent color
    def _update(self, actions):
        for k in actions.keys():
            # print(actions)
            agent_pos = actions[k]
            for p in agent_pos: # for multiple turns for the agent: just for testing purposes, in the real game, for each agent there is only one turn
                if(self.state_matrix[p[0], p[1]] == ""):
                    self._add_node(k, p)
                    # self._update_cycle(k, p)    # Update the conquer part if there is a cycle
                else:
                    print("You are trying to put in not empty node")
            # print(self._update_cycle(k, p))
        # print(self.state_matrix)
        # print("------------------------------")

    def step(self, actions):
        self._update(actions)
        obs  = self.get_observation()
        reward = self.get_reward()
        done = self.get_done()
        info = self.get_info()


        self.turn_counter += 1
        self.turn_counter %= len(self.agents)
        self.steps_counter += 1

        return obs, reward, done, info