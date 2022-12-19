import common_advent as advent
map = advent.get_input(__file__)

# graph based pathing because we are cool

def coordinate_to_val(cell: tuple):
    _row, _col = cell
    return elevation(map[_row][_col])

def elevation(char: chr):
    if char =='S':
        return 1
    elif char =='E':
        return 26
    else:
        return ord(char) - ord('a') + 1

def manhattan(location, end):
    return abs(end[0] - location[0]) + abs(end[1] - location[1])

def in_range(cell: tuple, target: tuple): # simplify our calls
    return in_h_range(target) and in_v_range(cell, target)

def in_h_range(target: tuple): # cell is (row, col), check if inside grid
     return True if target[0] in range(len(map)) and target[1] in range(len(map[0])) else False

def in_v_range(cell: tuple, target: tuple): # cell is (row, col), check if move is legal
    return True if coordinate_to_val(cell) + 1 >= coordinate_to_val(target) else False

def neighbors(cell: tuple):
    ortho_neighbors = [(-1,0), (1,0), (0,-1), (0,1)] # U, D, L, R
    neighbors = []
    for n in ortho_neighbors: # feels clunky?
        neighbors.append((cell[0]+n[0],cell[1]+n[1]))
    return neighbors

def find_endpoints(_map):
    S, E = None, None
    for i in range(len(_map)):
        if _map[i].find('S') > -1:
            S = (i, _map[i].find('S'))
        if _map[i].find('E') > -1:
            E = (i, _map[i].find('E'))
    assert S is not None and E is not None
    return S, E

for r in range(len(map)):
    for c in range(len(map[0])):
        print(f"{coordinate_to_val((r, c)):>2} ", end='')
    print()

S, E = find_endpoints(map)
te = neighbors(S)
print([in_range((0,0), n) for n in te])