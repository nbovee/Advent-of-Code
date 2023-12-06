import common_advent as advent
import re
input = advent.get_input(__file__)

def get_surrounding(point, input):
    pass   

def in_bound(point):
    r, c = point
    max_c = len(input[0])
    max_r = len(input)
    return True if  0 <= r < max_r and 0 <= c < max_c else False

def correct_bound(l_point, r_point):
    l_r, l_c = l_point
    r_r, r_c = r_point
    max_c = len(input[0])
    max_r = len(input)
    return (max(l_r, 0), max(l_c, 0)), (min(r_r, max_c), max(r_c, max_r))

pn_list = set()
p_list = set()
for row, line in enumerate(input):
    possible = re.finditer("\d+", line)
    for p in possible:
        p_list.add(int(p.group()))
        if int(p.group()) not in pn_list:
            search_area = []
            # technically we should be searching the string sections and not individual points
            # section = line[p.span()[0]-1:p.span()[1]+1]
            search_area_points = (row-1, p.span()[0]-1) , (row+1, p.span()[1]+1)
            for r in range(search_area_points[0][0],search_area_points[1][0]+1):
                for c in range(search_area_points[0][1],search_area_points[1][1]+1):
                    search_area.append((r,c))
            search_area = list(filter(in_bound, search_area))
            for point_r, point_c in search_area:
                if re.match("[^0-9.]", input[point_r][point_c]):
                    pn_list.add(int(p.group()))
                    break
# print(pn_list)
print(sum(pn_list))
print(p_list.difference(pn_list))