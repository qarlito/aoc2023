
#ordered_values = 'AKQJT98765432'[::-1]
ordered_values = 'AKQT98765432J'[::-1]

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

    cards_set = set(self.cards)
    if len(cards_set) == 1:
      self.score = SCORE5
    else:
      if 'J' not in handstr:
        self.score = self.get_score(self.cards)
      else:
        self.score = 0
        for i in cards_set.difference({0}):
          althand = Hand(self.handstr.replace('J', ordered_values[i]), self.bid)
          #print(f'{self.handstr} -> Try althand {althand.handstr} -> score {althand.score}')
          self.score = max(self.score, althand.score)

  def get_score(self, cards):

    cards_set = set(cards)
    if len(cards_set) == 1:
      return SCORE5
 
    if len(cards_set) == 2:
      if cards.count(cards[0]) in [1, 4]:
        return SCORE4
      else:
        return SCOREFH

    if len(cards_set) == 3:
      if cards.count(cards[0]) in (1,3) and cards.count(cards[1]) in (1,3):
        # 1 + 1 + 3
        return SCORE3
      else:
        # 2 + 2 + 1
        return SCORE2P

    if len(cards_set) == 4:
      return SCORE1P

    return SCORE0



s='''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

from advent_input_07 import s

# WRONG: 249071353

result = list()
for line in s.splitlines():
  handstr, bidstr = line.split()
  hand = Hand(handstr, int(bidstr))
  result.append((hand.score, hand.cards, hand.handstr, hand.bid))

#print(sorted(result))

total = 0
for i, (_, _, _, bid) in enumerate(sorted(result)):
    total = total + (i+1) * bid
print(f'TOTAL: {total}')
