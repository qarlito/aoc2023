
ordered_values = 'AKQJT98765432'[::-1]

SCORE5 = 10
SCORE4 = 9
SCOREFH = 8
SCORE3 = 7
SCORE2P = 6
SCORE1P = 5
SCORE0 = 4

class Hand:

  def __init__(self, handstr, bid):

    assert len(handstr) == 5
    for item in handstr:
      assert item in ordered_values

    self.handstr = handstr
    self.bid = bid
    self.cards = list(map(lambda c: ordered_values.index(c), handstr))
    self.cards_set = set(self.cards)
    self.score = self.get_score()

  def get_score(self):

    if len(self.cards_set) == 1:
      return SCORE5
 
    if len(self.cards_set) == 2:
      if self.cards.count(self.cards[0]) in [1, 4]:
        return SCORE4
      else:
        return SCOREFH

    if len(self.cards_set) == 3:
      if self.cards.count(self.cards[0]) in (1,3) and self.cards.count(self.cards[1]) in (1,3):
        # 1 + 1 + 3
        return SCORE3
      else:
        # 2 + 2 + 1
        return SCORE2P

    if len(self.cards_set) == 4:
      return SCORE1P

    return SCORE0



s='''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

from advent_input_07 import s

result = list()
for line in s.splitlines():
  handstr, bidstr = line.split()
  hand = Hand(handstr, int(bidstr))
  result.append((hand.score, hand.cards, hand.handstr, hand.bid))

print(sorted(result))

total = 0
for i, (_, _, _, bid) in enumerate(sorted(result)):
    total = total + (i+1) * bid
print(f'TOTAL: {total}')
