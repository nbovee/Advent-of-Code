import common_advent as advent
import re
input = advent.get_input(__file__)

def correct_bound(l_point, r_point):
    l_r, l_c = l_point
    r_r, r_c = r_point
    max_c = len(input[0])
    max_r = len(input)-1
    return (max(l_r, 0), max(l_c, 0)), (min(r_r, max_r), min(r_c, max_c))

pn_list = []
pn_re = re.compile(r"\d+")
symbol_re = re.compile(r"[^\d+.]")
gear_re = re.compile(r"\*")
for row, line in enumerate(input):
    possible = re.finditer(pn_re, line)
    for p in possible:
        p_int = int(p.group())
        s, e = correct_bound((row-1, p.span()[0]-1), (row+1, p.span()[1]+1))
        test_string = "".join([input[subrow][s[1]:e[1]] for subrow in range(s[0], e[0]+1)])
        if re.findall(symbol_re, test_string):
            pn_list.append(p_int)
print(sum(pn_list))

gear_score = 0
for row, line in enumerate(input):
    possible = re.finditer(gear_re, line)
    for p in possible:
        cogs = []
        index = p.span()[0]
        s, e = correct_bound((row-1, 0), (row+1, len(line)))
        test_string = list([input[subrow] for subrow in range(s[0], e[0]+1)])
        for r2 in test_string:
            for p2 in re.finditer(pn_re, r2):
                if not set(range(*p2.span())).isdisjoint(range(index - 1, index + 2)):
                    cogs.append(p2)
        if len(cogs)>=2:
            gear_score += int(cogs[0].group()) * int(cogs[1].group())

print(gear_score)