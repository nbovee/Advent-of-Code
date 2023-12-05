import re
import itertools
import common_advent as advent

sensor_response = advent.get_input(__file__)
# faster method is probably to have a 3 line window and parse intercepts for diamond pattern around a point
# ex:         #
#            #.#
#             #

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def process_line(_test_row, _segments_list, deep_pass = False, filter_set = None):
    intersects = [[] for x in range(4)]
    for c0, c1, c2, c3 in zip(_segments_list[0::4], _segments_list[1::4], _segments_list[2::4], _segments_list[3::4]): # U D L R
        if _test_row >= c0[0] and _test_row <=c1[0]: # check if intersects even possible
            intersects[0].append(find_segment_col_intersect(c0, c2, _test_row)) # // up-left
            intersects[1].append(find_segment_col_intersect(c0, c3, _test_row)) # \\ up-right
            intersects[2].append(find_segment_col_intersect(c2, c1, _test_row)) # \\ left-bottom
            intersects[3].append(find_segment_col_intersect(c3, c1, _test_row)) # // right-bottom
    if not deep_pass:
        intersects = [set(x) for x in intersects]
        combined_set = set()
        for one, two in itertools.combinations(intersects, 2): # six combinations
            one, two = set(one), set(two) # these start as lists
            combined_set = combined_set.union(one.intersection(two)) # intersects must appear in multiple intersect sets
        combined_set.discard(None)
        return combined_set.intersection(filter_set) if filter_set is not None else combined_set
    else: # do full processing without throwing all this data around
        occupied_set = set()
        for l, r in zip(*intersects[0:2]): # upper pair
            if l is not None and r is not None:
                occupied_set.update([x for x in range(l, r + 1)])
        for l, r in zip(*intersects[2:4]): # lower pair
            if l is not None and r is not None:
                occupied_set.update([x for x in range(l, r + 1)])
        return occupied_set.intersection(filter_set) if filter_set is not None else occupied_set

def find_segment_col_intersect(corner0, corner1, intersect_row):
    if intersect_row in range(corner0[0], corner1[0]+1): # if these aren't send in the right order it will fail. lower y val cell must be first
        offset = corner0[0] - intersect_row
        return corner0[1] + offset if corner0[1] > corner1[1] else corner0[1] - offset

segments_list = []
p1_row = 2000000
unique_p1_row_beacons = set()
max_range, min_range = 4000000, 0 # could advance manually since I am on a slow laptop
row_one, row_two, row_thr = set(), set(), set()
allowable_range_set = set(range(max_range + 1))

for i, response in enumerate(sensor_response):
    parsed = list(map(int, re.findall('-?[0-9]+', response)))
    sensor, beacon = (parsed[1], parsed[0]), (parsed[3], parsed[2]) # provided as c,r with how I like to think about these
    unique_p1_row_beacons.add(beacon) if beacon[0] == p1_row else 0
    dist = manhattan(sensor, beacon)
    segments_list.extend([(sensor[0]-dist, sensor[1]), (sensor[0]+dist, sensor[1]), (sensor[0], sensor[1]-dist), (sensor[0], sensor[1]+dist)]) # U D L R

print(len(process_line(p1_row, segments_list, deep_pass=True))- len(unique_p1_row_beacons)) #part 1

for i in range(min_range + 1, max_range + 1):
    if i % (max_range//100) == 0:
        print(f"{i/(max_range + 1):2.2%}")
    row_thr = process_line(i, segments_list, filter_set=allowable_range_set)
    if row_one.intersection(row_thr): # if intersections appear in these rows, all we need is to see if cell is filled in row two
            print(f"Candidate: {i - 1}")
            temp = process_line(i - 1, segments_list, deep_pass=True, filter_set=allowable_range_set) # Search all locations, memory intensive
            temp = allowable_range_set.difference(temp)
            if len(temp) == 1:
                val = temp.pop()
                print(f"Empty space found at : ({i - 1},{val}). Signal value {(i-1)+4000000*val}.")
                break # one solution is all we need
    row_one = row_two
    row_two = row_thr
