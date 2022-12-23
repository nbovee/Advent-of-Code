import re

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
test_row = 2000000

# faster method is probably to have a 3 line window and parse intercepts for diamond pattern around a point
# ex:      
#             #
#            #.#
#             #

def find_segment_col_intersect(corner0, corner1, intersect_row):
    if intersect_row in range(corner0[0], corner1[0]+1): # if these aren't send in the right order it will fail. lower y val cell must be first
        offset = corner0[0] - intersect_row
        return corner0[1] + offset if corner0[1] > corner1[1] else corner0[1] - offset

def iterate_segments(_test_row, second_mode = False):
    test_row = _test_row
    _occupied_set_in_row = set()
    for c0, c1, c2, c3 in zip(segments_list[0::4], segments_list[1::4], segments_list[2::4], segments_list[3::4]): # U D L R
        if test_row >= c0[0] and test_row <=c1[0]:
            intersect0_col = find_segment_col_intersect(c0, c2, test_row) # // up-left
            intersect1_col, intersect2_col, intersect3_col = None, None, None
            if intersect0_col is None:
                intersect2_col = find_segment_col_intersect(c2, c1, test_row) # \\ left-bottom
                intersect3_col = find_segment_col_intersect(c3, c1, test_row) # // right-bottom
                if not second_mode:
                    _occupied_set_in_row.update([x for x in range(max(0,intersect2_col), min(max_range,intersect3_col)+1)])
            else:
                intersect1_col = find_segment_col_intersect(c0, c3, test_row) # \\ up-right
                if not second_mode:
                    _occupied_set_in_row.update([x for x in range(max(0,intersect0_col), min(max_range,intersect1_col)+1)])
            if second_mode:
                _occupied_set_in_row.update([intersect0_col, intersect1_col, intersect2_col, intersect3_col]) # add only intersects and then find gaps of 2 for deeper processing
    if second_mode:
        _occupied_set_in_row.discard(None)
        for i in _occupied_set_in_row:
            if (i + 2 in _occupied_set_in_row and i + 1 not in _occupied_set_in_row): # could miss edges?
                val = iterate_segments(test_row) # second mode is false now
                print(f"Checked {test_row} with filled: {val} = {val*100//(max_range + 1)}%")
                break
    return(len(_occupied_set_in_row))

second_check = []
for i in range(max_range, -1, -1):
    if i % 100000 == 0:
        print(f"{i/(max_range + 1):2.2%}")
    filled = iterate_segments(i, second_mode=True)
    if filled == max_range: # narrow our search space for second pass
        print(i)
        print(filled)
        second_check.append(i)

print(second_check)
for i in second_check:
    pass