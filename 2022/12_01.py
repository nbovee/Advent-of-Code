import heapq

import common_advent as advent
map = advent.get_input(__file__)

# graph based pathing because we are cool

class Map():
    def __init__(self, map_list) -> None:
        self.map = map_list
        self.S, self.E = self.find_endpoints(self.map)
        self.cost = 1 # no other cost to travel to possible squares

    def find_endpoints(self, _map):
        S, E = None, None
        for i in range(len(_map)):
            if _map[i].find('S') > -1:
                S = (i, _map[i].find('S'))
            if _map[i].find('E') > -1:
                E = (i, _map[i].find('E'))
        assert S is not None and E is not None
        return S, E

    def set_startpoint(self, cell: tuple):
        self.S = cell

    def coordinate_to_val(self, cell: tuple):
        _row, _col = cell
        return self.elevation(map[_row][_col])

    def elevation(self, char: chr):
        if char =='S':
            return 1
        elif char =='E':
            return 26
        else:
            return ord(char) - ord('a') + 1

    def in_range(self, cell: tuple, target: tuple): # simplify our calls
        return self.in_h_range(target) and self.in_v_range(cell, target)

    def in_h_range(self, target: tuple): # cell is (row, col), check if inside grid
        return True if target[0] in range(len(map)) and target[1] in range(len(map[0])) else False

    def in_v_range(self, cell: tuple, target: tuple): # cell is (row, col), check if move is legal
        return True if self.coordinate_to_val(cell) + 1 >= self.coordinate_to_val(target) else False

    def straight_line(self, location: tuple, end: tuple):
        return ((end[0] - location[0])**2 + (end[1] - location[1])**2)**0.5

    def neighbors(self, cell: tuple):
        ortho_neighbors = [(-1,0), (1,0), (0,-1), (0,1)] # U, D, L, R
        neighbors = []
        for n in ortho_neighbors: # feels clunky?
            neighbors.append((cell[0]+n[0],cell[1]+n[1]))
        return filter(lambda n: self.in_range(cell, n), neighbors)

    def display(self, path):
        for r, row in enumerate(self.map):
            for c, col in enumerate(row):
                print('#',end='') if (r,c) in path else print(col,end='')
            print()
                    

class PriorityQ():
    def __init__(self) -> None:
        self.priority_heap = []
        self.tiebreaker = 0

    def __len__(self):
        return len(self.priority_heap)

    def add(self, priority, location):
        heapq.heappush(self.priority_heap, (priority, self.tiebreaker, location))
        self.tiebreaker += 1

    def next(self):
        return heapq.heappop(self.priority_heap)


class AStar():
    def __init__(self, map, fake_start = None) -> None:
        self.graph = map
        self.S = fake_start if fake_start is not None else self.graph.S
        self.parent_loc = {self.S: None}
        self.best_cost = {self.S: 0}
        self.pq = PriorityQ()
        self.heuristic = self.graph.straight_line
        self.goal_found = False
        self.path = None

    def find_path(self):
        self.pq.add(0, self.S)
        while len(self.pq) > 0:
            current = self.pq.next()[-1] # separate cell from the priority and tiebreaker values
            if current == self.graph.E:
                return True
            for next in self.graph.neighbors(current):
                cost = self.best_cost[current] + self.graph.cost
                if next not in self.best_cost or cost < self.best_cost[current]:
                    self.best_cost[next] = cost
                    self.parent_loc[next] = current
                    self.pq.add(cost + self.heuristic(next, self.graph.E), next)
        return False

    def return_path(self):
        if self.goal_found and self.path is not None :
            return self.path
        self.goal_found = self.find_path()
        step = self.graph.E
        self.path = []
        if self.goal_found == False:
            return None # makes our part 2 easier
        while step is not None and step != self.S:
            self.path.append(step)
            step = self.parent_loc[step]
        return self.path

m = Map(map)
a = AStar(m)

p1_path = a.return_path()
m.display(p1_path)
print(f"Length of path: {len(p1_path)}")

# part 2 quick hacks
hiking = []
for r, row in enumerate(map):
    for c, col in enumerate(row):
        if col == 'a':
            temp = AStar(m, fake_start=(r,c)).return_path()
            if temp is not None:
                heapq.heappush(hiking, len(temp))
print(f"Length of shortest possible path: {heapq.heappop(hiking)}")