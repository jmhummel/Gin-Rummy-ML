import random
from enum import Enum


class Suit(Enum):
    SPADES = 0
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3

    def __str__(self):
        d = {
            self.SPADES: 'S',
            self.DIAMONDS: 'D',
            self.CLUBS: 'C',
            self.HEARTS: 'H',
        }
        return d[self]


class Rank(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12

    def __str__(self):
        d = {
            self.ACE: 'A',
            self.TWO: '2',
            self.THREE: '3',
            self.FOUR: '4',
            self.FIVE: '5',
            self.SIX: '6',
            self.SEVEN: '7',
            self.EIGHT: '8',
            self.NINE: '9',
            self.TEN: 'T',
            self.JACK: 'J',
            self.QUEEN: 'Q',
            self.KING: 'K',
        }
        return d[self]


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        return self.value() < other.value()

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __repr__(self):
        return f'{self.rank}{self.suit}'

    def value(self):
        return self.suit.value * len(Suit) + self.rank.value

    @staticmethod
    def enumerate():
        return [Card(suit, rank) for suit in Suit for rank in Rank]

    @staticmethod
    def from_value(val):
        num_suits = len(Suit)
        suit = Suit(val / num_suits)
        rank = Rank(val % num_suits)
        return Card(suit, rank)


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

