import random
from enum import IntEnum

from gin_rummy.cards import Deck, Card
from mcts import Game


class CardState(IntEnum):
    STOCK = 0
    DISCARD = 1
    TOP_DISCARD = 2
    MY_HAND = 3
    OPP_HAND = 4


class Action(IntEnum):
    DRAW_STOCK = 0
    DRAW_DISCARD = 1
    PASS = 2
    KNOCK = 3

    @staticmethod
    def DISCARD(card: Card):
        return 4 + card.value()

    @staticmethod
    def get_discard_card(i: int) -> Card:
        val = i - 4
        return Card.from_value(val)

    def __len__(self):
        return 56  # 4 Enum states, 52 Discard states


class GinRummy(Game):
    def __init__(self, dealer=None):
        self.stock = Deck()
        self.dealer = dealer if dealer else random.choice([0, 1])
        self.hands = [[], []]
        self.discard_pile = []
        self.deal()
        self.turn = 1
        self.cur_player = self.get_opponent(self.dealer)
        self.is_first_upcard_taken = False

    @staticmethod
    def get_opponent(player):
        return 0 if player == 1 else 1

    def deal(self):
        deal_order = [self.get_opponent(self.dealer), self.dealer]
        for _ in range(10):
            for player in deal_order:
                card = self.stock.draw()
                self.hands[player].append(card)

        card = self.stock.draw()
        self.discard_pile.append(card)

    def draw_stock(self):
        card = self.stock.draw()
        self.hands[self.cur_player].append(card)

    def draw_discard(self):
        card = self.discard_pile.pop()
        self.hands[self.cur_player].append(card)

    def discard(self, card: Card):
        if card not in self.hands[self.cur_player]:
            raise Exception("Can't discard card not held in hand")
        self.hands[self.cur_player].remove(card)
        self.discard_pile.append(card)

    def get_cur_player(self):
        return self.cur_player

    def next_turn(self):
        self.turn += 1
        self.cur_player = self.get_opponent(self.cur_player)

    def can_knock(self):
        pass  # TODO

    def evaluate_knock(self):
        pass  # TODO

    def get_action_size(self):
        return len(Action)

    def get_valid_actions(self, player):
        valid_actions = [0] * self.get_action_size()
        if player != self.cur_player:
            return valid_actions

        if len(self.hands[player]) == 11:
            for card in self.hands[player]:
                valid_actions[Action.DISCARD(card)] = 1
            # TODO can knock?
            valid_actions[Action.KNOCK] = 1
            return valid_actions

        if (self.turn == 1 or self.turn == 2) and not self.is_first_upcard_taken:
            valid_actions[Action.DRAW_DISCARD] = 1
            valid_actions[Action.PASS] = 1
            return valid_actions

        if self.turn == 3 and not self.is_first_upcard_taken:
            valid_actions[Action.DRAW_STOCK] = 1
            return valid_actions

        valid_actions[Action.DRAW_STOCK] = 1
        valid_actions[Action.DRAW_DISCARD] = 1
        return valid_actions

    def take_action(self, action: int):
        if action == Action.DRAW_STOCK:
            self.draw_stock()
        elif action == Action.DRAW_DISCARD:
            self.draw_discard()
        elif action == Action.PASS:
            self.next_turn()
        elif action == Action.KNOCK:
            self.evaluate_knock()
        else:
            card = Action.get_discard_card(action)
            self.discard(card)
            self.next_turn()

    def get_observation_size(self):
        pass

    def get_observation(self, player: int):
        observation = [CardState.STOCK]*52
        for card in self.discard_pile[:-1]:
            observation[card.value()] = CardState.DISCARD
        for card in self.discard_pile[-1:]:
            observation[card.value()] = CardState.TOP_DISCARD
        for card in self.hands[player]:
            observation[card.value()] = CardState.MY_HAND
        for card in self.hands[self.get_opponent(player)]:
            observation[card.value()] = CardState.OPP_HAND

    def get_observation_str(self, observation: [int]):
        return str(observation)

    def is_ended(self):
        pass  # TODO

    def is_draw(self):
        pass  # TODO

    def get_score(self, player):
        pass  # TODO

    def clone(self):
        pass  # TODO



