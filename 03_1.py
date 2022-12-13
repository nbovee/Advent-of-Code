def priority(char):
    if char.islower():
        return ord(char) - ord('a') + 1
    else:
        return ord(char) - ord('A') + 27

data = [line.strip() for line in open("input/03.txt", "r").readlines()]

sum = 0
for bag in data:
    l, r = set(bag.strip()[:int(len(bag)/2)]), set(bag.strip()[int(len(bag)/2):])
    mistake = l.intersection(r).pop()
    sum += priority(mistake)
print(sum)

sum2 = 0
for elf0, elf1, elf2 in zip(data[::3],data[1::3],data[2::3]):
    badge = set(elf0).intersection(set(elf1).intersection(set(elf2))).pop()
    sum2 += priority(badge)
print(sum2)
    