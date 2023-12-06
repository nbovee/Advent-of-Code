get_input = lambda n: [l.strip('\n') for l in open('./2023/input/' + n.replace('\\','/').split('/')[-1][:2] + '.txt','r',encoding='utf-8').readlines()]
