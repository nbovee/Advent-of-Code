score = {
    'A X' : 4, # rock = rock
    'B X' : 1, # paper > rock
    'C X' : 7, # scissors < rock
    'A Y' : 8, # rock < paper
    'B Y' : 5, # paper = paper
    'C Y' : 2, # scissors > paper
    'A Z' : 3, # rock > scissors
    'B Z' : 9, # paper < scissors
    'C Z' : 6  # scissors = scissors
}
score2 = {
    'A X' : 3, # rock lose
    'B X' : 1, # paper lose
    'C X' : 2, # scissors lose
    'A Y' : 4, # rock draw
    'B Y' : 5, # paper draw
    'C Y' : 6, # scissors draw
    'A Z' : 8, # rock win
    'B Z' : 9, # paper win
    'C Z' : 7  # scissors win
}
sum = 0
with open("input/02.txt", "r") as input:
    for line in input:
        print(line, end='')
        sum+=score2[line.rstrip()]
print(sum)
