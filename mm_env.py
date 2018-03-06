import random
import itertools

class Env:
    def __init__(self):
        self.actions = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]

    def get_action(self, q, state, epsilon):
        """
        state will be given as a string of format "SEED-SEED", the possible actions will be the 
        2 different seeds.
        """
        action1 = state[:2]
        action2 = state[3:5]
        possible_actions = [action1, action2]
        r = random.random()
        if r < epsilon:
            action = random.choice(possible_actions)
        else:
            action = random.choice(possible_actions)
        #else:
         #   if q[(state, action1)] > q[(state, action2)]:
          #      action = action1
           # else:
            #    action = action2
        return action

    def step(self, action):
        """
        Moves to the next state and reward for the action
        """

        next_state = "{}-{}".format(action, action)
        reward = 1
        return reward, next_state

    def get_round_one(self):
        """
        Based the match, determine both possible options (i.e. team 1 wins or team 2 wins).
        
        Returns the 2 seeds and team IDs of the current match
        """
        #conference_dict = {"W": "East", "X": "Midwest", "Y": "South", "Z": "West"}
        first_round = ["01-16", "02-15", "03-14", "04-13", "05-12", "06-11", "07-10", "08-09"]

        return first_round
    
    def get_round_two(self, fr_actions):
        round_2 = []
        round_2.append("{}-{}".format(fr_actions[0], fr_actions[-1]))
        round_2.append("{}-{}".format(fr_actions[1], fr_actions[-2]))
        round_2.append("{}-{}".format(fr_actions[2], fr_actions[-3]))
        round_2.append("{}-{}".format(fr_actions[3], fr_actions[-4]))
        return round_2

    def get_round_three(self, second_r_actions):
        round_3 = []
        round_3.append("{}-{}".format(second_r_actions[0], second_r_actions[-1]))
        round_3.append("{}-{}".format(second_r_actions[1], second_r_actions[-2]))
        return round_3

    def get_round_four(self, third_r_actions):
        round_4 = []
        round_4.append("{}-{}".format(third_r_actions[0], third_r_actions[-1]))
        return round_4
