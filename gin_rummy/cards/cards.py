import random
from enum import Enum
from typing import List
from collections import defaultdict


class Suit(Enum):
    SPADES = 0
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3


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


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        return self.value() < other.value()

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

    @staticmethod
    def get_sets(cards: List['Card']):
        cards_by_rank = defaultdict(list)
        for card in cards:
            cards_by_rank[card.rank].append(card)
        sets = []
        for rank in cards_by_rank:
            if len(cards_by_rank[rank]) >= 3:
                sets.append(cards_by_rank[rank])
        return sets

    @staticmethod
    def get_runs(cards: List['Card']):
        cards_by_suit = defaultdict(list)
        for card in cards:
            cards_by_suit[card.suit].append(card)
        runs = []
        for suit in cards_by_suit:
            run = []
            for card in sorted(cards_by_suit[suit]):
                if not run:
                    run.append(card)
                elif card.rank.value == run[-1].rank.value + 1:
                    run.append(card)
                elif len(run) >= 3:
                    runs.append(run)
                    run = [card]
                else:
                    run = [card]
            if len(run) >= 3:
                runs.append(run)
        return runs


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

