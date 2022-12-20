from itertools import zip_longest
import common_advent as advent

results = advent.get_input(__file__)
results = [r for r in results if r != '']

def safe_eval_list(_input): # yolo, but safely
    return eval(_input, {"__builtins__":None}, {'list' : list})

def recursive_compare(_left, _right):
    if _left == -1 and _right != -1: # catch unequal lists
        return 1
    if _right == -1 and _left != -1: # catch unequal lists (we may not need this one, but lets be safe)
        return -1
    if isinstance(_left, int) and isinstance(_right, int):
        return _right -_left  # should be >0 if correct, 0 if further testing needed, <0 if incorrect
    if isinstance(_left, int) and isinstance(_right, list):
        return recursive_compare([_left], _right) # left int, right list (wrap left, recur)
    if isinstance(_left, list) and isinstance(_right, int):
        return recursive_compare(_left, [_right]) # left list, right int (wrap right, recur)
    if isinstance(_left, list) and isinstance(_right, list):
        for (l, r) in zip_longest(_left, _right, fillvalue=-1): # iterate to remove list shells simultaneously
            test = recursive_compare(l, r)
            if test != 0:
                return test
        return 0 # catch if truly equal, or if comparing [] and [] as they cannot be iterated
    raise Exception('And you may ask yourself, "Well, how did I get here?"')

def quick_sort(storage, l_index, r_index):
    
    def split(storage, _l_index, _r_index):
        _pivot = storage[_r_index]
        target = _l_index - 1
        for i in range(_l_index, _r_index):
            if recursive_compare(storage[i], _pivot) >= 0: # 1 is returned if left result is lower, ie left < pivot.
                target += 1
                storage[i], storage[target] = storage[target], storage[i]
        storage[target+1], storage[_r_index] = storage[_r_index], storage[target+1]
        return target + 1 # next pivot

    if l_index < r_index:
        pivot = split(storage, l_index, r_index)
        quick_sort(storage, l_index, pivot - 1)
        quick_sort(storage, pivot, r_index)

sum_good_packets = 0
fixed_packets = [[[2]], [[6]]] # start with dividers

for i, (left, right) in enumerate(zip(results[::2], results[1::2])):
    left, right, = safe_eval_list(left), safe_eval_list(right)
    test = recursive_compare(left, right)
    if test >= 0: # if in the correct order
        sum_good_packets += i + 1
        fixed_packets.extend([left, right])
    else: # incorrect order, test < 0
        fixed_packets.extend([right, left])

print(f"sum = {sum_good_packets:>6}")
quick_sort(fixed_packets, 0, len(fixed_packets)-1)
print(f"The part 2 thingy: {(fixed_packets.index([[6]])+1)*(fixed_packets.index([[2]])+1)}")
