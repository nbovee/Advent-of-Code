import common_advent as advent
instructions = advent.get_input(__file__)

class Rope(): # holds RopeSegments for convienance of display, they dont need it otherwise
    def __init__(self, length = 2) -> None:
        self.knots = [RopeSegment() for x in range(length)]
        for i in range(len(self.knots)-1):
            self.knots[i].assign_child(self.knots[i+1])
        
    tail_visited = lambda self, index: self.knots[index].knot_visited

    __str__ = lambda self: self.display_tail(len(self.knots)-1)
    
    def move(self, direction, count):
        for i in range(int(count)):
            self.knots[0].move_one(direction)
    
    def __update_display_bounds(self):
        self.display_bounds = [
            min(list(zip(*rope.tail_visited(0)))[0])-1,   # -x
            max(list(zip(*rope.tail_visited(0)))[0])+2,   # +x
            min(list(zip(*rope.tail_visited(0)))[1])-2,   # -y
            max(list(zip(*rope.tail_visited(0)))[1])+2    # +y
        ]

    def display_tail(self, index):
        self.__update_display_bounds()
        s = self.knots[index].tail_visited
        output = ''
        for col in range(self.display_bounds[2], self.display_bounds[3]):
            for row in range(self.display_bounds[0], self.display_bounds[1]):
                nchar = '#' if (row, col) in s else '.'
                for i in range(len(self.knots)-1,-1,-1): # reverse list for display priority
                    nchar = str(i+1) if self.knots[i].knot_loc == (row, col) else nchar
                nchar = 'H' if (row, col) == self.knots[0].head_loc else nchar
                nchar ='s' if (row, col) == (0,0) else nchar
                output += nchar
            output += '\n'
        return output.strip()

class RopeSegment():

    direction_dict = { # offsets in the display field rather than what humans expect row and column to be 
            'R' : (1,0),    # move right 1 in row (move over col)
            'U' : (0,-1),   # move into an earlier row (move in same col)
            'L' : (-1,0),   # move left 1 in row (move over col)
            'D' : (0,1)     # move 1 into a later row (move in same col)
        }
        
    def __init__(self, child = None) -> None: # child here for if we revisit to remove redundant head values in the rope
        self.knot_loc = (0,0)
        self.knot_visited = set()
        self.knot_visited.add(self.knot_loc)
        self.child = child

    def assign_child(self, child):
        self.child = child

    def add_coordinates(self, a, b): # tuple operation elementwise. I will not import numpy for advent unless forced to
        assert len(a) == len(b) == 2
        return (a[0] + b[0], a[1] + b[1]) #simple way for debugging

    def sub_coordinates(self, a, b):
        assert len(a) == len(b) == 2
        return (a[0] - b[0], a[1] - b[1]) #simple way for debugging

    __str__ = lambda self: str(self.knot_loc)
    __repr__ = __str__

    def move_one(self, direction):
        self.__set_knot_loc(self.add_coordinates(self.knot_loc, RopeSegment.direction_dict[direction]))

    def __set_knot_loc(self, new_location):
        self.knot_loc = new_location
        self.knot_visited.add(self.knot_loc)
        if self.child is not None:
            self.child.update_self(new_location)

    def update_self(self, new_head_location):
        row_dist, col_dist = self.sub_coordinates(new_head_location, self.knot_loc)
        new_knot_row, new_knot_col = 0, 0
        if abs(row_dist) == 2: # ortho move, single update
            new_knot_row = 1 if row_dist > 0 else -1
        if abs(col_dist) == 2: # ortho move, single update
            new_knot_col = 1 if col_dist > 0 else -1
        new_knot_row = 0 if row_dist == 0 else new_knot_row
        new_knot_col = 0 if col_dist == 0 else new_knot_col
        new_knot_location = self.add_coordinates(self.knot_loc, (new_knot_row, new_knot_col))
        self.__set_knot_loc(new_knot_location)

knots = 10        
rope = Rope(knots)
for instr in instructions:
    rope.move(*instr.split())
    
print(f"Rope with {2} knots tail occupancy: {len(rope.tail_visited(1))}")
print(f"Rope with {10} knots tail occupancy: {len(rope.tail_visited(knots-1))}")
# print(rope) # this is very pretty but the input given is too big to view nicely
