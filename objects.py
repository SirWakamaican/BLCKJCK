import random
import db


class Card:
    def __init__(self, suit, rank, points):
        self.suit = suit
        self.rank = rank
        self.points = points

    def __str__(self):
        str = "{r}{s}".format(r = self.rank, s = self.suit)
        return str

    def getPoints(self):
        return self.points


class Deck:
    def __init__(self):
        self.deck = []
        suit = ['H','D','S','C']
        rank = ['A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2]
        points = [1, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        for s in suit:
            for r in rank:
                card = Card(s, r, points[rank.index(r)])
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, counter, hand):
        for i in range(counter):
            hand.addCard(self.deck.pop(0))

    def count(self):
        return len(self.deck)

    def returnCard(self, usedCard):
        self.deck.append(usedCard)


class Hand:
    def __init__(self):
        self.hand = []

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(self.hand)-1:
            raise StopIteration()
        self.__index += 1
        card = self.hand[self.__index]
        return card

    def addCard(self, Card):
        self.hand.append(Card)

    def count(self):
        return len(self.hand)

    def total(self):
        total = 0
        for card in self.hand:
            total += card.getPoints()

        if total + 10 <= 21:
            for card in self.hand:
                if card.rank == "A":
                    total += 10
        return total

    def reset(self, Deck):
        for card in self.hand:
            Deck.returnCard(card)
            self.hand.remove(card)

    def show(self):
        return self.hand


class Session():
    def __init__(self, startTime, startMoney, stopTime, stopMoney):
        self.startTime = startTime
        self.stopTime = stopTime
        self.startMoney = startMoney
        self.stopMoney = stopMoney
