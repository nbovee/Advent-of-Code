import common_advent as advent
instructions = advent.get_input(__file__)

class Rope():
    def __init__(self, len) -> None:
        self.knots = [RopeSegment() for x in range(len)]
        
    tail_visited = lambda self, index: self.knots[index].tail_visited

    __str__ = lambda self: self.display_tail(len(self.knots)-1)
    
    def move(self, direction, count):
        for i in range(int(count)):
            self.__move_one(direction)

    def __move_one(self, direction):
        self.knots[0]._move_one(direction)
        for i in range(1, len(self.knots)):
            self.knots[i]._set_head_loc(self.knots[i-1].tail_loc) # set head to tail of previous, tail will catch up
    
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
                    nchar = str(i+1) if self.knots[i].tail_loc == (row, col) else nchar
                nchar = 'H' if (row, col) == self.knots[0].head_loc else nchar
                nchar ='s' if (row, col) == (0,0) else nchar
                output += nchar
            output += '\n'
        return output.strip()

class RopeSegment():
    def __init__(self, child = None) -> None: # child here for if we revisit to remove redundant head values in the rope
        self.head_loc, self.tail_loc = (0,0), (0,0)
        self.tail_visited = set()
        self.tail_visited.add(self.tail_loc)
        self.direction_dict = { # offsets in the display field rather than what humans expect row and column to be 
            'R' : (1,0),    # move right 1 in row (move over col)
            'U' : (0,-1),   # move into an earlier row (move in same col)
            'L' : (-1,0),   # move left 1 in row (move over col)
            'D' : (0,1)     # move 1 into a later row (move in same col)
        }
        
    def add_coordinates(self, a, b): # tuple operation elementwise. I will not import numpy for advent unless forced to
        assert len(a) == len(b) == 2
        return (a[0] + b[0], a[1] + b[1]) #simple way for debugging

    def sub_coordinates(self, a, b):
        assert len(a) == len(b) == 2
        return (a[0] - b[0], a[1] - b[1]) #simple way for debugging

    def _move_one(self, direction):
        self._set_head_loc(self.add_coordinates(self.head_loc, self.direction_dict[direction]))

    def _set_head_loc(self, new_location): # distances of new not checked, be careful
        self.__update_tail(new_location) # may need to reference old location
        self.head_loc = new_location 

    def __update_tail(self, new_head_location):
        row_dist, col_dist = self.sub_coordinates(new_head_location, self.tail_loc)
        new_tail_row, new_tail_col = 0, 0
        if abs(row_dist) == 2 and col_dist == 0: # ortho move, single update
                new_tail_row = 1 if row_dist > 0 else -1
        elif abs(col_dist) == 2 and row_dist == 0: # ortho move, single update
                new_tail_col = 1 if col_dist > 0 else -1
        elif abs(row_dist) + abs(col_dist) >= 3: # diag move, both require an update
            new_tail_row = 1 if row_dist > 0 else -1
            new_tail_col = 1 if col_dist > 0 else -1
        elif abs(row_dist) + abs(col_dist) <= 2: # skip if total magnitude is 2 or less (given that by now, one direction cannot be 2 magnitude)
            pass
        else:
            raise Exception("error updating a tail, check if attempting to move tail more than 1 step")
        new_tail_location = self.add_coordinates(self.tail_loc, (new_tail_row, new_tail_col))
        self.tail_loc = new_tail_location
        self.tail_visited.add(self.tail_loc)

segments = 9        
rope = Rope(segments)
for instr in instructions:
    rope.move(*instr.split())
    
print(f"Rope with {2} knots tail occupancy: {len(rope.tail_visited(0))}")
print(f"Rope with {10} knots tail occupancy: {len(rope.tail_visited(segments-1))}")
# print(rope) # this is very pretty but the input given is too big to view nicely
