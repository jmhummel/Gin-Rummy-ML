from operator import attrgetter
from typing import List
from gin_rummy.cards import Card
import logging

logger = logging.getLogger('knock_evaluation')


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
    for i, card in enumerate(cards[1:]):
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
    if not melds:
        return 0, []
    best_leaf = build_meld_tree(melds)
    best_score = best_leaf.deadwood
    best_melds = get_meld_set(best_leaf)
    return best_score, best_melds


def get_all_melds(cards: List[Card]) -> List[List[Card]]:
    all_melds = []

    # First, check for 4 card sets of the same-numbered card
    cards = sort_by_value(cards)
    for i in range(len(cards) - 3):
        pos_meld = cards[i:i+4]
        if is_set_meld(pos_meld):
            all_melds.append(pos_meld)
            # When a 4-card meld is found, also add all the possible 3-card melds which
            # won't be picked up by the subsequent 3-card scan.
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
    return all_melds


def calc_optimal_deadwood(cards: List[Card]):
    logger.info('calc_optimal_deadwood: ' + str(cards))
    all_melds = get_all_melds(cards)

    # Find the optimal set of melds.
    all_melds.sort(key=count_deadwood)
    logger.info('All melds:')
    for meld in all_melds:
        logger.info(meld)
    best_score, best_melds = get_best_combination(all_melds)
    deadwood = count_deadwood(cards) - best_score
    logger.info(f"Optimal melds: {' '.join([str(m) for m in best_melds])}")
    deadwood_cards = cards[:]
    for meld in best_melds:
        for card in meld:
            deadwood_cards.remove(card)
    logger.info(f"Deadwood: {', '.join([str(c) for c in sort_by_value(deadwood_cards)])} ({deadwood})")
    return deadwood, best_melds


def can_knock(cards: List[Card]):
    if len(cards) != 11:
        raise Exception("Should only be called with exactly 11 cards")

    deadwood, _ = calc_optimal_deadwood(cards)
    if deadwood <= 20:
        for i in range(len(cards)):
            hand = cards[:i] + cards[i+1:]
            logger.info("i: " + str(hand))
            deadwood, _ = calc_optimal_deadwood(hand)
            if deadwood <= 10:
                return True
    return False


def get_layable_melds(existing_melds: List[List[Card]], cards: List[Card]) -> List[List[Card]]:
    layable_melds = []

    # First, check 3 card sets of the same-numbered card
    existing_sets = [meld for meld in existing_melds if is_set_meld(meld) and len(meld) == 3]
    for set_meld in existing_sets:
        rank = set_meld[0].rank
        for card in cards:
            if card.rank.value == rank.value:
                layable_melds.append([card])

    # Next, check for runs in the same suit
    cards = sort_by_value(cards)
    existing_runs = [meld for meld in existing_melds if is_run_meld(meld)]
    for run_meld in existing_runs:
        suit = run_meld[0].suit
        start_rank = run_meld[0].rank
        end_rank = run_meld[-1].rank

        for i in range(len(cards)):
            if cards[i].suit.value == suit.value:
                if cards[i].rank.value == start_rank.value - 2 and i+1<len(cards) and cards[i+1].rank.value == start_rank.value - 1:
                    layable_melds.append([cards[i], cards[i+1]])
                if cards[i].rank.value == start_rank.value - 1:
                    layable_melds.append([cards[i]])
                if cards[i].rank.value == end_rank.value + 1:
                    layable_melds.append([cards[i]])
                if cards[i].rank.value == end_rank.value + 1 and i+1<len(cards) and cards[i+1].rank.value == start_rank.value + 2:
                    layable_melds.append([cards[i], cards[i+1]])




    cards = sort_by_value(cards)
    for i in range(len(cards) - 3):
        pos_meld = cards[i:i+4]
        if is_set_meld(pos_meld):
            all_melds.append(pos_meld)
            # When a 4-card meld is found, also add all the possible 3-card melds which
            # won't be picked up by the subsequent 3-card scan.
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
    return all_melds

def evaluate_knock(player_hand, opponent_hand):
    player_deadwood, player_melds = calc_optimal_deadwood(player_hand)

    # Calculate best melds for opponent, allowing lays extending player's melds
    cards_to_consider = opponent_hand[:]
    for meld in player_melds:
        cards_to_consider.extend(meld)
    all_melds = get_all_melds(cards_to_consider)
