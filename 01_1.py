# could also read entire file, split on '\n\n' to find elves, then map to list.
elves = [[]]
with open("input/01.txt", "r")as input:
    for line in input:
        i += 1
        if line == '\n':
            elves.append([])
        else:
            elves[-1].append(int(line.strip()))

total = 0
for i in range(3):
    chosen_elf = 0
    for i, elf in enumerate(elves):
        if sum(elf) > sum(elves[chosen_elf]):
            chosen_elf = i
    print(f"elf at {chosen_elf} has {sum(elves[chosen_elf])} calories")
    total += sum(elves.pop(chosen_elf))
print(total)