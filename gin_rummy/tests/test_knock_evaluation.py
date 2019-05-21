from gin_rummy.knock_evaluation import *
from gin_rummy.cards import Card, Suit, Rank
import unittest
import logging

logging.basicConfig(level=logging.DEBUG)


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
        deadwood, _ = calc_optimal_deadwood(self.hand)
        self.assertEqual(deadwood, 24)


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
        deadwood, _ = calc_optimal_deadwood(self.hand)
        self.assertEqual(deadwood, 14)

    def test_can_knock(self):
        self.assertTrue(can_knock(self.hand))


class TestKnockEvaluation3(unittest.TestCase):
    def setUp(self) -> None:
        self.player_hand = [
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.SIX),
        ]

        self.opponent_hand = [
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.FOUR),
        ]

    def test_evaluate_knock(self):
        evaluate_knock(self.player_hand, self.opponent_hand)
        # self.assertEqual(deadwood, 14)


if __name__ == '__main__':
    unittest.main()
