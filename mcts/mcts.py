from abc import abstractmethod


class Game:
    @abstractmethod
    def get_cur_player(self):
        """
        Returns:
            int: current player idx
        """
        pass

    @abstractmethod
    def get_action_size(self):
        """
        Returns:
            int: number of all possible actions
        """
        pass

    @abstractmethod
    def get_valid_actions(self, player):
        """
        Input:
            player: player
        Returns:
            validActions: a binary vector of length self.get_action_size(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        pass

    @abstractmethod
    def take_action(self, action):
        """
        Input:
            action: action taken by the current player
        Returns:
            double: score of current player on the current turn
            int: player who plays in the next turn
        """
        pass

    @abstractmethod
    def get_observation_size(self):
        """
        Returns:
            (x,y,z): a tuple of observation dimensions
        """
        pass

    @abstractmethod
    def get_observation(self, player):
        """
        Input:
            player: current player
        Returns:
            observation matrix which will serve as an input to agent.predict
        """
        pass

    @abstractmethod
    def get_observation_str(self, observation):
        """
        Input:
            observation: observation
        Returns:
            string: a quick conversion of state to a string format.
                    Required by MCTS for hashing.
        """
        pass

    @abstractmethod
    def is_ended(self):
        """
        This method must return True if is_draw returns True
        Returns:
            boolean: False if game has not ended. True otherwise
        """
        pass

    @abstractmethod
    def is_draw(self):
        """
        Returns:
            boolean: True if game ended in a draw, False otherwise
        """
        pass

    @abstractmethod
    def get_score(self, player):
        """
        Input:
            player: current player
        Returns:
            double: reward in [-1, 1] for player if game has ended
        """
        pass

    @abstractmethod
    def clone(self):
        """
        Returns:
            Game: a deep clone of current Game object
        """
        pass


class Agent:
    @abstractmethod
    def predict(self, game, game_player):
        """
        Returns:
            policy, value: stochastic policy and a continuous value of a game observation
        """
