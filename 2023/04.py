import common_advent as advent
import re
input = advent.get_input(__file__)

p1_score = 0
p2_cards = []         
card_dict = {}

for row, line in enumerate(input,1):
    _, card, hand = [set(elem.split()) for elem in re.split(r"[:|]", line)]
    wins = int(2**(len(card.intersection(hand))-1))
    p1_score += wins
    card_dict[row] = card, hand

p2_cards.extend([1 for _ in range(len(card_dict.keys()))])
print(p1_score)

for card_num, copies in enumerate(p2_cards, 1):
    card, hand = card_dict[card_num]
    matches = len(card.intersection(hand))
    for i in range(card_num+1, card_num+matches+1):
        p2_cards[i-1] = p2_cards[i-1] + copies
print(sum(p2_cards))