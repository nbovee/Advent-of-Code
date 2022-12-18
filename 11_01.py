import common_advent as advent
instructions = advent.get_input(__file__)
import operator
import re
import copy

class Monkey(): # that funky monkey

    monkeys = [] # they all know each other
    master_monkey_mega_modulus = 1
    operator_dict = {'*' : operator.mul, '+' : operator.add}
    external_worry = lambda n : n

    def set_worry_func(func):
        Monkey.external_worry = func

    def play(rounds = 0):
        Monkey.link_monkeys()
        for i in range(rounds):
            for monkey in Monkey.monkeys:
                monkey.execute_turn()

    def link_monkeys():
        for monkey in Monkey.monkeys:
            assert monkey.true_index < len(Monkey.monkeys) and monkey.false_index < len(Monkey.monkeys)
            monkey.true = Monkey.monkeys[monkey.true_index]
            monkey.false = Monkey.monkeys[monkey.false_index]
            Monkey.master_monkey_mega_modulus *= monkey.test

    def __init__(self, lines) -> None:
        self.name = lines[0].strip(':').split(' ')[-1]
        self.items = list(map(int,re.findall('[0-9]+', lines[1])))
        self.op = Monkey.operator_dict[lines[2].split(' ')[-2]]
        self.op_val = lines[2].split(' ')[-1]
        self.test = int(re.findall('[0-9]+', lines[3])[-1])
        self.true_index = int(re.findall('[0-9]+', lines[4])[-1])
        self.false_index = int(re.findall('[0-9]+', lines[5])[-1])
        Monkey.monkeys.append(self)
        self.items_thrown = 0
    
    __str__ = lambda self: ' a monkey named ' + self.name + ' holding ' + self.items
    
    def items_thrown(self):
        return self.items_thrown

    def __catch_item(self, item):
        self.items.append(item)

    def execute_turn(self):
        while self.items:
            item = self.items.pop(0)
            val = int(self.op_val) if 'old' != self.op_val else item # inspect
            item = self.op(item, val)
            item = Monkey.external_worry(item)
            self.items_thrown += 1
            self.true.__catch_item(item) if item % self.test == 0 else self.false.__catch_item(item)

for i in range(0,len(instructions),7):
    Monkey(instructions[i:i+7])
copy_monkeys = copy.deepcopy(Monkey.monkeys) # easy reset
Monkey.set_worry_func(lambda n : n//3)

Monkey.play(20)
m1 = operator.mul(*sorted(list(map(Monkey.items_thrown, Monkey.monkeys)), key = lambda n:-n)[:2])

Monkey.monkeys = copy_monkeys
Monkey.set_worry_func(lambda n : n % Monkey.master_monkey_mega_modulus)

Monkey.play(10000)
m2 = operator.mul(*sorted(list(map(Monkey.items_thrown, Monkey.monkeys)), key = lambda n:-n)[:2])

print(f"Monkey Business 1 : {m1}\nMonkey Business 2 : {m2}")