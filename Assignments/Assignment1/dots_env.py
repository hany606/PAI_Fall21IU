import numpy as np
from Network import Network
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon



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
        self.num_steps = 0
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
        if(self.num_steps >= self.max_num_step):
            return True
        return False

    def get_info(self):
        return {}

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
                self._update_cycle(agent, point)    # Update the conquer part if there is a cycle
                # print(f"Add edge {point} -> {p}, dist={self._dist(point,p)}")
                # print(f"Ids {self.network.get_id(*point)} -> {self.network.get_id(*p)}")

    def _add_node(self, agent, point):
        self.state_matrix[point[0], point[1]] = agent[0]
        self.network.add_node(point[0], point[1], agent, agent)
        self._add_edges(agent, point)

    def _conquer_node(self, agent, point):
        self.state_matrix[point[0], point[1]] = agent[0]
        self.network.modify_node(point[0], point[1], agent, agent)
        self._add_edges(agent, point)



    def _get_coords(self, cycles):
        coords = []
        for cycle in cycles:
            coords.append([])
            for s in cycle:
                split = s.split(',')
                split = tuple([int(sp) for sp in split])
                coords[-1].append(split)
        return coords

    def raycast(self, agent, cycle):
        # Source: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
        def ccw(A,B,C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        # Return true if line segments AB and CD intersect
        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        # for each node in the graph
        for i in range(self.width):
            for j in range(self.height):
                if(self.state_matrix[i, j] == "" or self.state_matrix[i, j] == agent[0]):   # if is empty or already captured by that agent that has cycle
                    continue
                # if it is not empty and for the opponent player
                else:
                    point = [i,j]
                    num_intersections = int(intersect(point, [point[0], self.width+1], cycle[-1], cycle[0]))
                    # for each consecutive poitns, create a segment
                    for k in range(len(cycle)-1):
                        # for each segment in the convex polygon, check if it is intersected or not
                        num_intersections += int(intersect(point, [point[0], self.width+1], cycle[k], cycle[k+1]))
                    # Source: https://www.wikiwand.com/en/Point_in_polygon#/Ray_casting_algorithm
                    if(num_intersections % 2 > 0):
                        print(f"Point: {point} is inside {cycle} for agent {agent}")
                        print("------------------------------------------------------")
                        self._conquer_node(agent, point)
                        # if(self.state_matrix[i, j] == "" or self.state_matrix[i, j] == agent[0]):
                        #     self._conquer_node(agent, point)
                        # if(self.state_matrix[i, j] == ""):
                        #     self._add_node(agent, point)
                        # point = Point(*point)
                        # polygon = Polygon(cycle)
                        # print(polygon.contains(point))
                


    # TODO: this can be optimized better in order not to check old cycles and old nodes -> just check the new generated ones
    # It will be only called if a new edge was added
    def _update_cycle(self, agent, node):
        cycles = self.network.find_cycles(agent, node)
        if(len(cycles) > 0):
            # print(len(cycles), agent, cycles)
            cycles_coords = self._get_coords(cycles)
            # print(len(cycles_coords), agent, cycles_coords)
            # Check if there is a node inside this cycle or not, if there is then conquer
            for cycle in cycles_coords:
                self.raycast(agent, cycle)  # cycle for that agent

        # return len(cycles)

    # TODO: if there is a cycle then add all the nodes inside that cycle
    # Actions is dictionary with key the agent id -> agent color
    def _update(self, actions):
        for a in actions.keys():
            # print(actions)
            agent_pos = actions[a]
            for p in agent_pos: # for multiple turns for the agent: just for testing purposes, in the real game, for each agent there is only one turn
                if(self.state_matrix[p[0], p[1]] == ""):
                    self._add_node(a, p)
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
        self.num_steps += 1

        return obs, reward, done, info