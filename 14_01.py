from itertools import zip_longest
import common_advent as advent

rock_locations = advent.get_input(__file__)

sand_drop = 500

rock_set = set()

def add_rock():
    pass

print(list(
    zip_longest(
        [x for x in range(10)],[x for x in range(2,2+1)]
        )))