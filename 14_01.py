import common_advent as advent

rock_locations = advent.get_input(__file__)

class Cave():
    def __init__(self, sand_loc, floor = False) -> None:
        self.sand_drop = sand_loc    # O---> +r   given cells are in (r, c) form
        self.source = '+'            # |
        self.sand = 'o'              # V
        self.rock = '#'              # +c
        self.air = ' '
        self.area_bounds = [0, 1, 0, 1] # row- row+ col- col+ 
        self.occupied_dict = {self.sand_drop: self.source}
        self.sand_count = 0
        self.floor = floor
        self.floor_row = None

    def add_element(self, location, material):
        if location not in list(self.occupied_dict.keys()):
            self.occupied_dict[location] = material
            r_key_list = [r for (r, c) in self.occupied_dict.keys()]
            c_key_list = [c for r, c in self.occupied_dict.keys()]
            c_min_height = min(c_key_list)
            c_max_height = max(c_key_list) + 2 # overestimate to use as floor later as well
            r_min_height = min(r_key_list)
            r_max_height = max(r_key_list) + 1
            self.area_bounds = [r_min_height, r_max_height, c_min_height, c_max_height]

    def __str__(self) -> str:
        out = ''
        for c in range(self.area_bounds[2], self.area_bounds[3] + 1):
            for r in range(self.area_bounds[0], self.area_bounds[1] + 1):
                if (r, c) in self.occupied_dict.keys():
                    out += self.occupied_dict[(r, c)]
                else:
                    out += self.air
            out += '\n'
        return out

    def add_rock(self, start_point:tuple, end_point:tuple):
        if start_point > end_point: # reorder elements to make iteration happy
            start_point, end_point = end_point, start_point
        s_r, s_c = start_point
        for r in range(abs(start_point[0] - end_point[0]) + 1): # bidirectional
            for c in range(abs(start_point[1] - end_point[1]) + 1):
                self.add_element((r + s_r, c + s_c), self.rock)
        self.floor_row = self.area_bounds[3]

    def next_vertical_occupied(self, location): # speed up solution by searching ahead for collision.
        (_r, _c) = location # could hardcall source
        for c in range(_c + 1, self.area_bounds[3]+1):
            if (_r, c) in list(self.occupied_dict.keys()):
                return _r, c - 1 # 1 above the occupied
        return (_r, self.floor_row) - 1 if self.floor is True else None # either the item falls into space, or hits an infinite floor

    def slide_stop(self, location):
        _r, _c = location
        oc = list(self.occupied_dict.keys())
        b_left, below, b_right = (_r - 1, _c + 1), (_r, _c + 1), (_r + 1, _c+ 1)
        if _c == self.floor_row - 1:
            return location if self.floor is True else None # either we are in the void or inf. floor
        if below in oc:
            if b_left in oc:
                if b_right in oc:
                    return location # end motion, still on map
                else:
                    return b_right # slide right
            else:
                return b_left # slide left
        else:
            return self.next_vertical_occupied(location) # continue down, use next_vertical_occupied to skip unnecessary checks.

    def drop_sand(self):
        _location = []
        next_location = self.sand_drop
        while next_location is not None and next_location != _location:
            next_location = self.slide_stop(_location:= next_location) # if equal, stop, else update
        if next_location is None or next_location == self.sand_drop:
            return False # halt here
        self.add_element(next_location, self.sand)
        self.sand_count += 1
        return True # continue

c1 = Cave((500, 0))
c2 = Cave((500, 0), floor=True)

for line in rock_locations:
    l = line.split(' -> ')
    for i in range(len(l)-1):
        t = tuple(map(int,l[i].split(',')))
        t1 = tuple(map(int,l[i+1].split(',')))
        c1.add_rock(t, t1)
        c2.add_rock(t, t1)
print(c1) # pretty

def crunch(cave, display = False):
    while(cave.drop_sand()): pass
    if display:
        print(cave)
    return cave.sand_count # indicates successful placement

print(f"Amount of sand to overflow map: {crunch(c1)}")

# currently we exit rather than cover the source block, so off by one. Could cover this case but more lines so eh
print(f"Amount of sand to cover source location: {crunch(c2) + 1}")
