from gin_rummy import can_knock
from gin_rummy.cards import Card, Suit, Rank


def main():
    hand = [
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

    print(can_knock(hand))


if __name__ == '__main__':
    main()
