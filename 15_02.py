import re
import itertools

import common_advent as advent

sensor_response = advent.get_input(__file__)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

sensor_disp = 'S'
beacon_disp = 'B'
empty_disp = '#'
sensor_dict = {}
occupied_dict = {}
segments_list = []


for i, response in enumerate(sensor_response):
    parsed = list(map(int, re.findall('-?[0-9]+', response)))
    sensor, beacon = (parsed[1], parsed[0]), (parsed[3], parsed[2]) # these might be backwards? assumed r,c  - c,r seems better
    occupied_dict[sensor] = sensor_disp
    occupied_dict[beacon] = beacon_disp
    sensor_dict[sensor] = beacon
    dist = manhattan(sensor, beacon)
    # print(f"Sensor pair #{i+1} manhattan distance is {dist}.")
    
    segments_list.extend([(sensor[0]-dist, sensor[1]), (sensor[0]+dist, sensor[1]), (sensor[0], sensor[1]-dist), (sensor[0], sensor[1]+dist)]) # U D L R

display_bounds = advent.display_bounds(set(segments_list)) # bounds for row- row+ col- col+ 

max_range = 4000000

# faster method is probably to have a 3 line window and parse intercepts for diamond pattern around a point
# ex:      
#             #
#            #.#
#             #

def find_segment_col_intersect(corner0, corner1, intersect_row):
    if intersect_row in range(corner0[0], corner1[0]+1): # if these aren't send in the right order it will fail. lower y val cell must be first
        offset = corner0[0] - intersect_row
        return corner0[1] + offset if corner0[1] > corner1[1] else corner0[1] - offset

def intersects_in_line(_test_row):
    test_row = _test_row
    _occupied_set_in_row = set()
    intersects = [set() for x in range(4)]
    for c0, c1, c2, c3 in zip(segments_list[0::4], segments_list[1::4], segments_list[2::4], segments_list[3::4]): # U D L R
        if test_row >= c0[0] and test_row <=c1[0]: # check if intersects even possible
            intersects[0].add(find_segment_col_intersect(c0, c2, test_row)) # // up-left
            intersects[1].add(find_segment_col_intersect(c0, c3, test_row)) # \\ up-right
            intersects[2].add(find_segment_col_intersect(c2, c1, test_row)) # \\ left-bottom
            intersects[3].add(find_segment_col_intersect(c3, c1, test_row)) # // right-bottom
    for one, two in itertools.combinations(intersects, 2): # six combinations
        temp = one.intersection(two)
        _occupied_set_in_row= _occupied_set_in_row.union(temp) # add only intersects that appear at least in two different lines
    if len(_occupied_set_in_row) > 0:
        i = []
    _occupied_set_in_row.discard(None)
    return _occupied_set_in_row


min_range = 0
row_one = intersects_in_line(min_range - 0)
row_two = intersects_in_line(min_range - 1)
row_thr = None
candidates = set()
test_set = set([x for x in range(max_range + 1)])


for i in range(min_range + 2, max_range + 1):
    row_thr = intersects_in_line(i)
    # print(list(row_thr.intersection(test_set)))
    if test_set.intersection(row_one).intersection(row_thr):
        # if {cell + 1, cell - 1} in row_two and cell not in row_two: # diamond pattern candidacy
            print(f"Candidate: {i}")
            candidates.add(i)
            # break # one possibility is all we need
    row_one = row_two
    row_two = row_thr
    if i % (max_range//100) == 0:
        print(f"{i/(max_range + 1):2.2%}")

print(candidates) # 
candidates = {2380928, 2380930, 3230813}
print(candidates) # 

def iterate_segments(_test_row):
    test_row = _test_row
    _occupied_set_in_row = set()
    for c0, c1, c2, c3 in zip(segments_list[0::4], segments_list[1::4], segments_list[2::4], segments_list[3::4]): # U D L R
        if test_row >= c0[0] and test_row <=c1[0]:
            intersect0_col = find_segment_col_intersect(c0, c2, test_row) # // up-left
            intersect1_col = find_segment_col_intersect(c0, c3, test_row) # \\ up-right
            intersect2_col = find_segment_col_intersect(c2, c1, test_row) # \\ left-bottom
            intersect3_col = find_segment_col_intersect(c3, c1, test_row) # // right-bottom
            if intersect2_col is not None:
                _occupied_set_in_row.update([x for x in range(intersect2_col, intersect3_col+1)])
            if intersect0_col is not None:
                _occupied_set_in_row.update([x for x in range(intersect0_col, intersect1_col+1)])
    filter_set = set(range(0,max_range + 1))
    return _occupied_set_in_row.intersection(filter_set)


test_set = set([x for x in range(max_range + 1)])
for candidate in candidates:
    temp = iterate_segments(candidate)
    print(len(temp))
    print(len(test_set.difference(temp)))