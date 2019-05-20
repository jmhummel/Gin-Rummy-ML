from operator import attrgetter
from typing import List
from gin_rummy.cards import Card


def point_value(card: Card) -> int:
    v = card.rank.value + 1
    if v > 10:
        return 10
    return v


def count_deadwood(cards: List[Card]) -> int:
    return sum([point_value(card) for card in cards])


def is_run_meld(cards: List[Card]):
    if len(cards) < 3:
        return False
    suit = cards[0].suit
    rank = cards[0].rank
    for i, card in enumerate(cards):
        if card.suit != suit or card.rank.value != rank.value + i + 1:
            return False
    return True


def is_set_meld(cards: List[Card]):
    if len(cards) < 3:
        return False
    rank = cards[0].rank
    for card in cards:
        if card.rank != rank:
            return False
    return True


def sort_by_value(cards: List[Card]):
    """ Returns cards sorted first by number value, then by suit """
    return sorted(cards, key=attrgetter('rank.value', 'suit.value'))


def sort_by_suit(cards: List[Card]):
    """ Returns cards sorted first by suit, then by number value """
    return sorted(cards, key=attrgetter('suit.value', 'rank.value'))


class MeldNode:
    def __init__(self, meld, parent=None):
        self.parent = parent
        self.meld = meld
        self.deadwood = count_deadwood(meld)
        if parent:
            self.deadwood += parent.deadwood


def clean_meld_group(melds, meld):
    """ Returns a new array of melds, containing all melds from the initial group,
        except for ones that contain cards from the given meld. """
    meld_group = []
    excluded_cards = set(meld)
    return [m for m in melds if set(m).isdisjoint(excluded_cards)]


def build_meld_tree(melds, root=None):
    """
    Returns the leaf node for which parent pointers can be followed to obtain the
    best possible meld combinations.
    This could be a O(n!) algorithm, where n is the number of melds. But in
    normal use, it shouldn't ever approach something too infeasible, because any
    large set of melds should include an enormous amount of overlapping melds,
    which will be eliminated from recursive calls. The max recursion depth will
    be equal to the largest number of non-overlapping melds.
    """
    best = root
    for meld in melds:
        node = MeldNode(meld, root)
        tree = build_meld_tree(clean_meld_group(melds, meld), node)
        if not best or tree.deadwood > best.deadwood:
            best = tree
    return best


def get_meld_set(leaf_node):
    """ Follows a path up to the root, and gets an array of melds """
    arr = []
    node = leaf_node
    while node:
        arr.append(node.meld)
        node = node.parent
    return arr


def get_best_combination(melds):
    best_leaf = build_meld_tree(melds)
    best_score = best_leaf.deadwood
    best_melds = get_meld_set(best_leaf)
    return best_score, best_melds


def calc_optimal_deadwood(cards: List[Card]):
    all_melds = []

    # First, check for 4 card sets of the same-numbered card
    cards = sort_by_value(cards)
    for i in range(len(cards) - 3):
        pos_meld = cards[i:i+4]
        if is_set_meld(pos_meld):
            all_melds.append(pos_meld)
            # When a 4-card meld is found, also add all the possible 3-card melds which
            # won't be picked up by the subsequent 3-card scan.
            print(pos_meld)
            all_melds.append([pos_meld[j] for j in [0, 1, 3]])
            all_melds.append([pos_meld[j] for j in [0, 2, 3]])

    # Next, check for 3 card sets of the same-numbered card
    for i in range(len(cards) - 2):
        pos_meld = cards[i:i+3]
        if is_set_meld(pos_meld):
            all_melds.append(pos_meld)

    # Next, check for 3 card runs in the same suit
    cards = sort_by_suit(cards)
    for i in range(len(cards) - 2):
        pos_meld = cards[i:i+3]
        if is_run_meld(pos_meld):
            all_melds.append(pos_meld)

    # Next, check for 4 card runs
    cards = sort_by_suit(cards)
    for i in range(len(cards) - 3):
        pos_meld = cards[i:i+4]
        if is_run_meld(pos_meld):
            all_melds.append(pos_meld)

    # Next, check for 5 card runs
    cards = sort_by_suit(cards)
    for i in range(len(cards) - 4):
        pos_meld = cards[i:i+5]
        if is_run_meld(pos_meld):
            all_melds.append(pos_meld)

    # 6 or more card run are equivalent to multiple smaller runs.

    # All possible melds have been found. Now, find the optimal set of melds.
    all_melds.sort(key=count_deadwood)
    best_score, best_melds = get_best_combination(all_melds)
    deadwood = count_deadwood(cards) - best_score
    print("Optimal melds: ")
    for meld in best_melds:
        print(meld)
        for card in meld:
            cards.remove(card)
    print("Deadwood: ")
    print(sort_by_value(cards))
    return deadwood


def can_knock(cards: List[Card]):
    if len(cards) == 10:
        return calc_optimal_deadwood(cards) <= 10
    else:
        # 11 cards, need to discard one
        if calc_optimal_deadwood(cards) <= 20:
            for i in range(len(cards)):
                if calc_optimal_deadwood(cards[:i] + cards[i+1:]) <= 10:
                    return True
        return False
