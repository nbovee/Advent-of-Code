import common_advent as advent
instructions = advent.get_input(__file__)

class Rope():
    def __init__(self, len) -> None:
        self.knots = [Knot() for x in range(len)]
        self.tail_visited = self.knots[-1].tail_visited
    
    def move(self, direction, count):
        for i in range(int(count)):
            self._move_one(direction)

    def _move_one(self, direction):
        self.knots[0]._move_one(direction)
        for i in range(1, len(self.knots)):
            # set head to tail of previous, tail will catch up
            self.knots[i]._set_head_loc(self.knots[i-1].tail_loc)


class Knot():
    def __init__(self) -> None:
        self.max_dist = 1
        self.head_loc = (0,0)
        self.tail_loc = (0,0)
        self.tail_visited = set()
        self.tail_visited.add(self.tail_loc)

        self.direction_dict = {
            'R' : (0,1),
            'U' : (1,0),
            'L' : (0,-1),
            'D' : (-1,0)
        }

    def __str__(self) -> str:
        return f"H:{self.head_loc} T:{self.tail_loc}"
        
    __repr__ = __str__
        
    def add_coordinates(self, a, b):
        assert len(a) == len(b) == 2
        return tuple(i + j for i,j in zip(a,b))

    def get_distance(self, a, b):
        return self.add_coordinates(a, tuple(-1*e for e in b))
    
    def _set_head_loc(self, new_location): # distances of new not checked, be careful
        self.update_tail(new_location, self.head_loc)
        self.head_loc = new_location 

    def move(self, direction, count):
        for i in range(int(count)):
            self._move_one(direction)

    def _move_one(self, direction):
        assert direction in self.direction_dict.keys()
        new_head_loc = self.add_coordinates(self.head_loc, self.direction_dict[direction])
        self.update_tail(new_head_loc, self.head_loc)
        self.head_loc = new_head_loc

    def update_tail(self, new_head_location, old_head_location):
        col_dist, row_dist = self.get_distance(new_head_location, self.tail_loc)
        if abs(row_dist) <= 1 and abs(col_dist) <= 1 or abs(col_dist) <= 1 and abs(row_dist) <= 1:
            pass # range
        elif (abs(row_dist) == 1 and abs(col_dist) == 1): # in diagonal range
            pass
        elif abs(row_dist) == 2 and col_dist == 0 or abs(col_dist) == 2 and row_dist == 0: # ortho move
            self.tail_loc = old_head_location # direct follow
        elif abs(row_dist) >= 1 and abs(col_dist) >= 1:# diag move, possible to see both values at 2 due to rope chaining
            new_tail_row, new_tail_col = 0, 0
            new_tail_row = 1 if row_dist > 0 else -1
            new_tail_col = 1 if col_dist > 0 else -1
            self.tail_loc = self.add_coordinates(self.tail_loc, (new_tail_col, new_tail_row))
        else:
            raise Exception("desync'd somehow, probably with _set_head_loc()")
        self.tail_visited.add(self.tail_loc)
    
rope1 = Rope(1)
rope9 = Rope(9)
for instr in instructions:
    rope1.move(*instr.split())
    rope9.move(*instr.split())
print(len(rope1.tail_visited))
print(len(rope9.tail_visited))


