import common_advent as advent
import re
input = advent.get_input(__file__)

test_set = {'red' :12, 'green' :13, 'blue' :14}
line_re = "|".join(["\d+ red", "\d+ green", "\d+ blue"])

def day2():
    game_dict = {}  
    for line in input:
        game_dict[int(re.findall("\d+", line)[0])] = re.findall(line_re, line)
    sum = 0
    sum2 = 0
    for game, shown in game_dict.items():
        temp = {'red' :0, 'green' :0, 'blue' :0}
        for set in shown:
            v, k = set.split(" ")
            if int(v) > temp[k]:
                temp[k] = int(v)
        internal = 1
        for v in temp.values():
            internal *= v
        sum2 += internal
        if temp['red'] <= test_set['red'] and temp['green'] <= test_set['green'] and temp['blue'] <= test_set['blue']:
            sum += int(game)
    print(f"1:{sum}\t2:{sum2}")

day2()