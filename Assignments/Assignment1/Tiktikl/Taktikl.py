# Note: the scripts were written to be easily for extension for multiple players game later

import numpy as np
from Network import Network
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon



# Actions: coordinate of the block
# Observation: {"world":state_matrix, "agent_turn"}

# Blue is the white, red is the black
class Taktikl:
    def __init__(self, 
                 width=4, 
                 height=4,
                 agents=["blue", "red"],
                 agents_colors={"blue":"blue", "red":"red"},
                 max_num_step=100,
                 node_size=5):
        
        self.width = width
        self.height = height
        self.agents = agents
        self.agents_colors = agents_colors
        self.turn_counter = 0
        self.num_steps = 0
        self.max_num_step = max_num_step
        self.node_size = node_size
        self.network = Network(width, height, node_size=node_size)
        self.scores = {a:0 for a in agents}
        self.agents_id = {a:a[0] for a in agents}
        self.STATE_EMPTY = ""

        self.reset()
    
    def other_opponents(self, agent):
        return [a for a in self.agents if a != agent]

    def get_agent_id(self, agent):
        return self.agents_id[agent]
    
    def get_agent(self, agent_id):
        for k in self.agents_id.keys():
            if(self.agents_id[k] == agent_id):
                return k

    def get_possible_actions(self):
        # Sample possible actions for the agent who has the turn
        # actions (current cell filled with the agent and the move)
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        actions = []
        for i in range(self.width):
            for j in range(self.height):
                if(self.state_matrix[i,j] == self.get_agent_id(self.other_opponents(self.get_turn())[0])): # if it is the other agent
                    continue
                if(self.state_matrix[i,j] == self.STATE_EMPTY): # it is an empty cell
                    continue
                for d in directions:
                    p = [[i,j][k]+d[k] for k in range(2)]
                    if(p[0] >= self.width or p[1] >= self.height or p[0] < 0 or p[1] < 0):
                        continue
                    # print(self.state_matrix[p[0], p[1]], self.state_matrix[point[0], point[1]], agent)
                    if(self.state_matrix[p[0], p[1]] == self.STATE_EMPTY): # it is an empty cell
                        actions.append([(i,j), d])

        return actions
        
    # Note: Must be called at first
    def reset(self):
        self.turn_counter = 0
        self.num_steps = 0
        self.state_matrix = np.zeros((self.width, self.height), dtype=str)
        self.network = Network(self.width, self.height, node_size=self.node_size)
        self._add_node("red", (0,3))
        self._add_node("red", (2,3))
        self._add_node("red", (1,0))
        self._add_node("red", (3,0))

        self._add_node("blue", (1,3))
        self._add_node("blue", (3,3))
        self._add_node("blue", (0,0))
        self._add_node("blue", (2,0))
        return self.get_observation()

    def render(self, timeout=0.0001):
        self.network.draw(timeout=timeout)
        
    def get_turn(self):
        return self.agents[self.turn_counter]

    def get_observation(self):
        obs = {"world": self.state_matrix, "turn": self.get_turn()}
        return obs

    def get_scores(self):
        winner = self.get_winner()
        if(winner is None):
            return 0
        elif(winner == self.agents[0]): # blue -> maximizer
            return 10
        else:                           # red -> minimizer
            return -10

    # TODO: Write it later in a better way without a lot of if conditions
    def get_winner(self):
        def get_check_3(l):
            if(len(l) == 3):
                return sum(l) == 3
            for i in range(2):
                if(sum(l[i:]) == 3):
                    return True

            return False

        # Check rows
        for a in self.agents:
            a_id = self.get_agent_id(a)
            for j in range(self.height):
                cols = []
                for i in range(self.width):
                    if(self.state_matrix[i,j] == a_id):
                        cols.append(1)
                    else:
                        cols.append(-1)
                    if(get_check_3(cols)):
                        # print(self.state_matrix)
                        # print(f"Winner Row: {j}")   # Because the r,c is y,x in grid
                        return a

            for i in range(self.width):
                rows = []
                for j in range(self.height):
                    if(self.state_matrix[i,j] == a_id):
                        rows.append(1)
                    else:
                        rows.append(-1)

                    if(get_check_3(rows)):
                        # print(self.state_matrix)
                        # print(f"Winner Col: {j}")
                        return a
                
            diag = [[],[],[]]
            for i in range(self.width):
                if(self.state_matrix[i,i] == a_id):
                    diag[0].append(1)
                else:
                    diag[0].append(-1)
                
            for i in range(self.width-1):
                diag[1].append(self.state_matrix[i,i+1] == a_id)
                diag[2].append(self.state_matrix[i+1,i] == a_id)
                if(True in [get_check_3(d) for d in diag]):
                    # print(f"Diag {diag}")
                    return a

            diag = [[],[],[]]
            for i in range(self.width):
                if(self.state_matrix[self.width-i-1,i] == a_id):
                    diag[0].append(1)
                else:
                    diag[0].append(-1)
            for i in range(self.width-1):
                diag[1].append(self.state_matrix[self.width-i-1,i+1] == a_id)
                diag[2].append(self.state_matrix[self.width-i-2,i] == a_id)
                if(True in [get_check_3(d) for d in diag]):
                    # print(f"Diag {diag}")
                    return a
        return None

    # Just for testing 
    def get_done(self):
        if(self.get_winner() is not None):
            return True
        return False

    def get_info(self):
        return {}

    def _add_node(self, agent, point):
        self.state_matrix[point[0], point[1]] = self.get_agent_id(agent)
        self.network.add_node(point[0], point[1], agent, agent)

    def _move_node(self, agent, point, new_point):
        self._add_node(agent, new_point)
        self.network.remove_node(point[0], point[1])
        self.state_matrix[point[0], point[1]] = self.STATE_EMPTY

    # Actions is dictionary with key the agent id -> agent color
    def _update(self, actions):
        for a in actions.keys():
            # print(actions)
            old_pos = actions[a][0]
            new_pos = [actions[a][1][i] + actions[a][0][i] for i in range(2)] 
            if(self.state_matrix[new_pos[0], new_pos[1]] == self.STATE_EMPTY):
                self._move_node(a, old_pos, new_pos)
                # self._update_cycle(k, p)    # Update the conquer part if there is a cycle
            else:
                print(f"({a})You are trying to put in not empty node")
                return {"error":"not_empty_node"}
            # print(self._update_cycle(k, p))
        # print(self.state_matrix)
        # print("------------------------------")
        return {"error":""}

    def decrease_counter(self):
        self.turn_counter = len(self.agents)
        self.turn_counter -= 1

    def step(self, actions):
        info = self._update(actions)
        scores = self.get_scores()
        done = self.get_done()
        # info = self.get_info(info)
        if(info["error"] == ''):
            self.turn_counter += 1
            self.turn_counter %= len(self.agents)
            self.num_steps += 1
        
        obs  = self.get_observation()

        return obs, scores, done, info