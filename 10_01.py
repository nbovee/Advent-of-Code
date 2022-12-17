import common_advent as advent
instructions = advent.get_input(__file__)

def signal_processing(_instructions, _responses, display = False):  
    
    cycle, x = 0, 1
    out = ''

    def draw_range(dist = 1, width = 40):
        base = cycle % width
        return True if x in list(range(base - dist, base + dist + 1)) else False

    for instruction in _instructions:
        cycle_step = 1
        if 'noop' in instruction:
            delta = 0
        else:
            delta = int(instruction.split()[-1])
            cycle_step += 1
            
        for i in range(cycle_step):
            out+= '#' if draw_range() else ' '
            cycle += 1
            if cycle in _responses:
                yield x * cycle # yield before applying value from prev cycle
        x += delta
    for i in range(0,240,40):
        print(out[i:i+40])

intervals = [20, 60, 100, 140, 180, 220]
l1 = list(signal_processing(instructions, intervals, display = True))
print(f"Sum of interval responses for part 1: {sum(l1)}")
