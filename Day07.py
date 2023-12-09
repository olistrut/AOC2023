import time
from collections import Counter

cardvalues = {"A": 14, "K": 13, "Q": 12, "X": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "J": 1}

def cmp_hands(hand):
    return hand.value

def calcTypeValue(part, cards):
    frequencies = Counter(cards)
    frequencies = dict(sorted(frequencies.items(), key=lambda x:x[1], reverse = True))


    if part == 2:
        # replace J with most frequent and highest valued "not J" unless cards = "JJJJJ". if "JJJJJ" replace with "AAAAA"
        if cards == "JJJJJ":
            cards = "AAAAA"
        else:
            if "J" in frequencies: del frequencies["J"]
            maxKey = "J"
            for i in range(len(frequencies.values())):
                # iterate over all cards with the same frequency as the most frequent card
                if list(frequencies.values())[i] == list(frequencies.values())[0]:
                    if cardvalues[list(frequencies.keys())[i]] > cardvalues[maxKey]:
                        maxKey = list(frequencies.keys())[i]

            cards = cards.replace("J", maxKey)

    pattern = sorted(Counter(cards).values(), reverse=True)
    value = [ [1,1,1,1,1], [2,1,1,1], [2,2,1], [3,1,1], [3,2], [4,1], [5] ].index(pattern)

    return [value], cards

class Hand:
    def __init__(self, part, cards, bid):
        if part == 1:
            cards = cards.replace("J", "X")

        self.cards = cards
        self.bid = bid
        self.value, self.converted = calcTypeValue(part, cards)

        for i in range(0,5):
            self.value.append(cardvalues[self.cards[i]])

    def __str__(self):
        return " Value:  "+str(self.value)+" Cards: " + str(self.cards)  +" (Converted to: "+self.converted+")"+" Bid: " + str(self.bid)

def solve(filename):
    result1 = 0
    result2 = 0

    f = open(filename)
    lines = f.readlines()

    hands1 = []
    hands2 = []

    for i, l in enumerate(lines):
        cards = l.split()[0]
        bid = int(l.split()[1])
        hands1.append(Hand(1, cards, bid))
        hands2.append(Hand(2, cards, bid))

    hand_sorted = sorted(hands1, key = cmp_hands)
    for i, h in enumerate(hand_sorted):
        # print("Rank: ", i+1, h)
        result1 += (i+1)*h.bid

    hand_sorted = sorted(hands2, key = cmp_hands)
    for i, h in enumerate(hand_sorted):
        # print("Rank: ", i+1, h)
        result2 += (i+1)*h.bid

    return result1, result2



start = time.time()
filename = "input/input07-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input07.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
