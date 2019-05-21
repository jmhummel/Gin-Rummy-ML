from gin_rummy.knock_evaluation import *
from gin_rummy.cards import Card, Suit, Rank
import unittest
import logging

# logging.basicConfig(level=logging.DEBUG)


class TestKnockEvaluation(unittest.TestCase):
    def setUp(self) -> None:
        self.hand = [
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.FOUR),
        ]

    def test_calc_optimal_deadwood(self):
        self.assertEqual(calc_optimal_deadwood(self.hand), 24)


class TestKnockEvaluation2(unittest.TestCase):
    def setUp(self) -> None:
        self.hand = [
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.NINE),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.FOUR),
        ]

    def test_calc_optimal_deadwood(self):
        self.assertEqual(calc_optimal_deadwood(self.hand), 14)

    def test_can_knock(self):
        self.assertTrue(can_knock(self.hand))


if __name__ == '__main__':
    unittest.main()
