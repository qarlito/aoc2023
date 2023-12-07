

s='''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

from advent_input_04 import s

def process_card(cardstr):
    card_info, card_content = cardstr.split(':')
    winning_numbers_str, my_numbers_str = card_content.split('|')
    winning_numbers = set(map(int, winning_numbers_str.strip().split()))
    my_numbers = set(map(int, my_numbers_str.strip().split()))
    winners = winning_numbers.intersection(my_numbers)
    if len(winners) == 0:
        return 0
    else:
        return 1 << (len(winners)-1)


result = 0
for cardstr in s.splitlines():
    card_score = process_card(cardstr)
    result += card_score


print(result)

