get_input = lambda n: [l.strip('\n') for l in open('./input/' + n.replace('\\','/').split('/')[-1][:2] + '.txt','r',encoding='utf-8').readlines()]

def display_bounds(set_of_coordinates):
    r_key_list = [r for r, c in set_of_coordinates]
    c_key_list = [c for r, c in set_of_coordinates]
    c_min_height = min(c_key_list)
    c_max_height = max(c_key_list) + 1 
    r_min_height = min(r_key_list)
    r_max_height = max(r_key_list) + 1
    return [r_min_height, r_max_height, c_min_height, c_max_height] # bounds for row- row+ col- col+ 