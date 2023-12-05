assignment = [line.strip().split(',') for line in open("input/04.txt", "r").readlines()]

fulloverlap = 0
partialoverlap = 0
for elves in assignment:
    elf0, elf1 = [list(map(int, elf.split('-'))) for elf in elves]
    if min(elf0) <= min(elf1) and max(elf0) >= max(elf1) or min(elf0) >= min(elf1) and max(elf0) <= max(elf1): 
        fulloverlap += 1
    if max(elf0) >= min(elf1) and min(elf0) <= max(elf1) or max(elf1) >= min(elf0) and min(elf0) >= max(elf1):
        partialoverlap += 1
    
print(fulloverlap)
print(partialoverlap)