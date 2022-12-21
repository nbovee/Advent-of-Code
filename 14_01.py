import common_advent as advent

rock_locations = advent.get_input(__file__)

class Cave():
    def __init__(self, sand_loc, floor = False) -> None:
        self.source_location = sand_loc    # O---> +r   given cells are in (r, c) form
        self.source = '+'                  # |
        self.sand = 'o'                    # V
        self.rock = '#'                    # +c
        self.air = ' '
        self.occupied_dict = {}
        self.sand_count = 0
        self.has_floor = floor
        self.floor_row = None
        self.add_element(self.source_location, self.source) # will create self.area_bounds 

    def add_element(self, _location, material):
        if _location not in list(self.occupied_dict.keys()) and material != self.air: # as is, air does not take occupy space
            self.occupied_dict[_location] = material
            r_key_list = [r for r, c in self.occupied_dict.keys()]
            c_key_list = [c for r, c in self.occupied_dict.keys()]
            c_min_height = min(c_key_list)
            c_max_height = max(c_key_list) + 2 # overestimate to use as floor later as well
            r_min_height = min(r_key_list)
            r_max_height = max(r_key_list) + 1
            self.area_bounds = [r_min_height, r_max_height, c_min_height, c_max_height] # row- row+ col- col+ 
            self.sand_count += 1 if material == self.sand else 0

    def __str__(self) -> str:
        out = ''
        for c in range(self.area_bounds[2], self.area_bounds[3] + 1):
            for r in range(self.area_bounds[0], self.area_bounds[1] + 1):
                if (r, c) in self.occupied_dict.keys():
                    out += self.occupied_dict[(r, c)]
                else:
                    out += self.air
            out += '\n'
        return out[:-1]

    def add_rock(self, start_point:tuple, end_point:tuple): # will draw a box instead of a diagonal if endpoints not orthagonally aligned
        if start_point > end_point: # reorder elements to make iteration happy
            start_point, end_point = end_point, start_point
        for r in range(abs(start_point[0] - end_point[0]) + 1):
            for c in range(abs(start_point[1] - end_point[1]) + 1):
                self.add_element((r + start_point[0], c + start_point[1]), self.rock)
        self.floor_row = self.area_bounds[3]

    def furthest_vertical_unoccupied(self, _location): # speed up solution by searching ahead for collision.
        for c in range(_location[1] + 1, self.area_bounds[3]+1):
            if (_location[0], c) in list(self.occupied_dict.keys()):
                return _location[0], c - 1 # 1 above the occupied
        return (_location[0], self.floor_row) - 1 if self.has_floor is True else None # either the item falls into space, or hits an infinite floor

    def slide_stop(self, _location):
        oc = list(self.occupied_dict.keys())
        b_left, below, b_right = (_location[0] - 1, _location[1] + 1), (_location[0], _location[1] + 1), (_location[0] + 1, _location[1]+ 1)
        if _location[1] == self.floor_row - 1:
            return _location if self.has_floor is True else None # either we are in the void or inf. floor
        if below in oc:
            if b_left in oc:
                if b_right in oc:
                    return _location # end motion, still on map
                else:
                    return b_right # slide right
            else:
                return b_left # slide left
        else:
            return self.furthest_vertical_unoccupied(_location) # continue down, use function to skip unnecessary checks.

    def drop_sand(self):
        _location = []
        next_location = self.source_location
        while next_location is not None and next_location != _location:
            next_location = self.slide_stop(_location:= next_location) # if equal, stop, else update
        if next_location is None or next_location == self.source_location:
            return False # halt here
        self.add_element(next_location, self.sand)
        return True # continue

cave_1 = Cave((500, 0))
cave_2 = Cave((500, 0), floor=True)

for line in rock_locations:
    l = line.split(' -> ')
    for i in range(len(l)-1):
        t = tuple(map(int,l[i].split(',')))
        t1 = tuple(map(int,l[i+1].split(',')))
        cave_1.add_rock(t, t1)
        cave_2.add_rock(t, t1)
print(cave_1) # pretty

def crunch(cave: Cave, display = False):
    while(cave.drop_sand()): pass
    if display:
        print(cave)
    return cave.sand_count # indicates successful placement

print(f"Amount of sand to overflow map: {crunch(cave_1)}")
print(f"Amount of sand to cover source location: {crunch(cave_2) + 1}") # currently we exit rather than cover the source block, so off by one. Could cover this case but more lines so eh
