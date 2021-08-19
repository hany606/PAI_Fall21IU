import numpy as np
from Network import Network


# Actions: coordinate of the block
# Observation: {"world":state_matrix, "agent_turn"}

class Dots:
    def __init__(self, 
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                 agents_colors=[[0,0,255], [255,0,0]],
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

    def render(self, timeout=100):
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

    # Actions is dictionary with key the agent id -> agent color
    def _update(self, actions):
        for k in actions.keys():
            agent_pos = actions[k]
            self.state_matrix[agent_pos[0], agent_pos[1]] = k
            self.network.add_node(agent_pos[0], agent_pos[1], k, k)

        self._create_cycles()
        self._update_cycle()

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