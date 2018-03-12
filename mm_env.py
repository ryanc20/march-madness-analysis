import random
import itertools
import mm_data

class Env:
    def __init__(self):
        self.actions = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]

    def get_action(self, q, state, epsilon, ff=False):
        """
        An action is chosen in an epsilon greedy fashion. A random number between 0 and 1
        is generated, if that value is less than epsilon, a random value is chosen. If the
        value is greater than epsilon but less than (epsilon + .01) (1% chance) the user predicts
        the winner of the matchup. Otherwise the max q value is chosen between the two possible
        actions aka teams playing eachother.
        """
        if ff == True:
            action1 = state[:3]
            action2 = state[4:7]
        else:
            action1 = state[:2]
            action2 = state[3:5]

        possible_actions = [action1, action2]
        
        #Random number between 0 and 1
        r = random.uniform(0, 1)
        
        #Picks an action 
        if r < epsilon:
            action = random.choice(possible_actions)
        elif r >= epsilon and r < epsilon + .01:
            action = input("Who is more likely to win? {}, {}, or IDK\n".format(action1, action2))
            if action == "IDK":
                action = random.choice(possible_actions)
        else:
            s_a_key1 = "{}-{}".format(state, action1)
            s_a_key2 = "{}-{}".format(state, action2)
            if q[s_a_key1] > q[s_a_key2]:
                action = action1
            else:
                action = action2

        return action

    def get_reward(self, action, year, conf, data, round_number):
        """
        Returns reward for the action based on if the action is in the next state.
        The chosen reward values are subject to change, perhaps to mimick how the 
        points are rewarded on a real bracket for March Madness.
        """
        #No idea why, but had to cast them to be strings, QUITE annoying of an error to figure out.
        round_1, round_2, round_3, round_4, winner = data.get_tourney_rounds(str(conf), str(year))
        
        flag = False
        if round_number == 1:
            for matchup in round_2:
                #print("ACTION: {}, MATCHUP: {}".format(action, matchup))
                if action in matchup:
                    flag = True
            if flag == True:
                reward = 10
            else:
                reward = -25

        elif round_number == 2:
            for matchup in round_3:
                if action in matchup:
                    flag = True
            if flag == True:
                reward = 20
            else:
                reward = -50

        elif round_number == 3:
            for matchup in round_4:
                if action in matchup:
                    flag = True
            if flag == True:
                reward = 30
            else:
                reward = -75

        elif round_number == 4:
            if action in winner:
                flag = True
            if flag == True:
                reward = 40
            else:
                reward = -100

        return reward

    def get_round_one(self):
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
