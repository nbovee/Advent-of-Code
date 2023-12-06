get_input = lambda n: [l.strip('\n') for l in open('./2023/input/' + n.replace('\\','/').split('/')[-1][:2] + '.txt','r',encoding='utf-8').readlines()]

# def in_bound(point, _input):
#     r, c = point
#     max_c = len(_input[0])
#     max_r = len(_input)
#     return True if  0 <= r < max_r and 0 <= c < max_c else False

# def correct_bound(l_point, r_point, _input):
#     l_r, l_c = l_point
#     r_r, r_c = r_point
#     max_c = len(_input[0])
#     max_r = len(_input)
#     return (max(l_r, 0), max(l_c, 0)), (min(r_r, max_c), max(r_c, max_r))