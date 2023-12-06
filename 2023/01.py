import common_advent as advent
import re
input = advent.get_input(__file__)

conv = {
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9',
}

val_re = re.compile("|".join(conv.values()))

key_val_list = []
for x in conv.items():
    key_val_list.extend(x)
key_val_re = re.compile("|".join(key_val_list))

def day1(regex, replace = dict()):
    sum = 0
    for i in input:
        rep = re.findall(regex, i)
        if replace:
            for e, r in enumerate(rep):
                if r in replace:
                    rep[e] = replace[r]
        sum += int(f"{rep[0]}{rep[-1]}")
    return sum

print(day1(val_re))
print(day1(key_val_re, replace=conv))