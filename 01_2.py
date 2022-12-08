# efficiency pass
import heapq
# structure for elves[ elf[[priority], ...]
elves = [] 
with open("input/01.txt", "r")as input:
    elves = list((map(int, line.strip().split('\n'))) for line in input.read().split('\n\n'))
elves = [[-sum(elf), elf] for elf in elves]
heapq.heapify(elves)
total = 0
for i in range(3):
    total += abs(heapq.heappop(elves)[0])
print(total)