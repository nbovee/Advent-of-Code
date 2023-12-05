import common_advent as advent
from math import prod
forest = advent.get_input(__file__)
forest = [list(map(int,line)) for line in forest]

def get_row_halves(index, data): # leftmost is always the tree for comparison
    row, col = index
    return data[row][col::-1], data[row][col:]

def get_col_halves(index, data): # leftmost is always the tree for comparison
    data = list(zip(*data)) 
    col, row = index # zip flips these
    return get_row_halves((row, col), data)

def is_visible(tree_input):
    tree = tree_input[0]
    val = all(tree_input[x] < tree for x in range(1,len(tree_input)))
    return val
    
def view_range(tree_input):
    tree, other_trees = tree_input[0], tree_input[1:]
    other_trees = list(map(lambda n: 1 if n>= tree else 0, other_trees)) # filter for trees >= tree
    return other_trees.index(1) + 1 if 1 in other_trees else len(other_trees) # view to tree + index offset, or full view to edge

def get_views(index):
    return *get_row_halves(index, forest), *get_col_halves(index, forest)

visible_count = 0
highest_scenic_score = 0

for i in range(len(forest)):
    for j in range(len(forest[0])):
        visible_count += 1 if len(list(filter(is_visible,get_views((i,j))))) > 0 else 0
        candidate = prod(map(view_range,get_views((i,j))))
        highest_scenic_score = candidate if candidate > highest_scenic_score else highest_scenic_score

print(f"{visible_count} visible trees")
print(f"most scenic tree: {highest_scenic_score}")