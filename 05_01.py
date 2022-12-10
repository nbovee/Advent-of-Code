import regex as re
import copy

stacks = [[] for i in range(9)] #offset by 1 from instructions
stacks2 = []

instruct_mode = False

file = open("input/05.txt", "r").readlines()

for line in file:
    if not instruct_mode:
        if line == '\n':
            instruct_mode = True
            stacks2 = copy.deepcopy(stacks)
        else:
            row = list(line)[1::4] #ez game
            for crate, stack in zip(row, stacks):
                if crate.isalpha():
                    stack.insert(0, crate)
    # do the thing
    else:
        num, source, target = list(map(int, re.findall('[0-9]+', line)))
        # part 1
        for i in range(num):
            stacks[target-1].extend(stacks[source-1].pop())
        # part 2
        move = stacks2[source-1][-num:]
        stacks2[source-1] = stacks2[source-1][:len(stacks2[source-1]) - num]
        stacks2[target-1].extend(move)

for stack in stacks:
    print(stack[-1],end='')
print()
    
for stack in stacks2:
    print(stack[-1],end='')
