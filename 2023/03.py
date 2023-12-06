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
potential_list = set()
pn_re = re.compile(r"\d+")
symbol_re = re.compile(r"[^\d.]")
for row, line in enumerate(input):
    possible = re.finditer(pn_re, line)
    for p in possible:
        p_int = int(p.group())
        potential_list.add(p_int)
        s, e = correct_bound((row-1, p.span()[0]-1), (row+1, p.span()[1]+1))
        test_string = "".join([input[subrow][s[1]:e[1]] for subrow in range(s[0], e[0]+1)])
        print(test_string)            
        if re.findall(symbol_re, test_string):
            pn_list.append(p_int)
print(sum(pn_list))
