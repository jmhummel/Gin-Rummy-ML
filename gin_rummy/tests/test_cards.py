from gin_rummy.cards import Card, Suit, Rank
import unittest
import logging

logging.basicConfig(level=logging.DEBUG)


class TestSuit(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_1(self):
        suit1 = Suit.SPADES
        suit2 = Suit.SPADES
        self.assertTrue(suit1 == suit2)

    def test_2(self):
        suit1 = Suit.SPADES
        suit2 = Suit.SPADES
        suit_set = {suit1}
        self.assertTrue(suit2 in suit_set)


class TestRank(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_1(self):
        rank1 = Rank.ACE
        rank2 = Rank.ACE
        self.assertTrue(rank1 == rank2)

    def test_2(self):
        rank1 = Rank.ACE
        rank2 = Rank.ACE
        rank_set = {rank1}
        self.assertTrue(rank2 in rank_set)


class TestCard(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_1(self):
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        self.assertTrue(card1 == card2)

    def test_2(self):
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        card_set = {card1}
        self.assertTrue(card2 in card_set)

    def test_3(self):
        card1 = Card(Suit.SPADES, Rank.ACE)
        card1_value = card1.value()
        card2 = Card.from_value(card1_value)
        self.assertTrue(card1 == card2)

    def test_4(self):
        card1 = Card(Suit.SPADES, Rank.ACE)
        card1_value = card1.value()
        card2 = Card.from_value(card1_value)
        self.assertTrue(card1.value() == card2.value())


if __name__ == '__main__':
    unittest.main()
