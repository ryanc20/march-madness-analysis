import numpy as np
import gym
from collections import defaultdict

import mm_data
import mm_env

class QAgent:
    def __init__(self, epsilon, alpha, gamma):
        self.q = defaultdict(lambda: 0)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.env = mm_env.Env()
        self.data = mm_data.TourneyData()

    def epsilon_greedy_train(self):
        """
        The state will be the matchup (i.e. seed 1 vs seed 16), and the action will
        be the team that won the match. The reward for the (state, action) pair will
        be determined by comparing it to what ACTUALLY happened in that years 
        March Madness tournament. The agent will be trained on each of the years (1985-2016)
        to update potential reward values for the selected action.
        
        In an attempt to account for the randomness of March Madness an epsilon greedy
        approach is used, where if the randomly generated value between 0 and 1 is less
        than the selected value of epsilon, it will select a random action, otherwise
        it will pick the action with the highest reward.
        """
        total_reward = 0

        for year in range(1985, 2016):
            final_four = []
            championship = []
            conferences = {"W": "East", "X": "Midwest", "Y": "South", "Z": "West"}

            for conf in conferences:
                print("CONFERENCE: {}, YEAR: {}".format(conferences[conf], year))

                round_1  = self.env.get_round_one()
                print("ROUND1:", round_1)

                first_r_actions = []
                for state in round_1:        
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 1)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += self.alpha * reward
                    #print("REWARD: {}".format(reward))
                    first_r_actions.append(action)
                 
                round_2 = self.env.get_round_two(first_r_actions)
                print("ROUND2:", round_2)

                second_r_actions = []
                for state in round_2:
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 2)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += reward
                    #print("REWARD: {}".format(reward))
                    second_r_actions.append(action)
                
                round_3 = self.env.get_round_three(second_r_actions)
                print("ROUND3:", round_3)

                third_r_actions = []
                for state in round_3:
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 3)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += self.alpha * reward
                    #print("REWARD: {}".format(reward))
                    third_r_actions.append(action)

                round_4 = self.env.get_round_four(third_r_actions)
                print("ROUND4:", round_4)

                fourth_r_actions = []
                for state in round_4:
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 4)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += self.alpha * reward
                    #print("REWARD: {}".format(reward))
                    fourth_r_actions.append(action)
                
                final_four.append("{}{}".format(conf, fourth_r_actions[0]))
                print("WINNER:", fourth_r_actions)
            print("TOTAL REWARD AFTER YEAR {} = {}".format(year, total_reward))
            formatted_final_four = []
            formatted_final_four.append("{}-{}".format(final_four[0], final_four[-1]))
            formatted_final_four.append("{}-{}".format(final_four[1], final_four[-2]))
            print("FINAL FOUR:", formatted_final_four)

            for state in formatted_final_four:
                action = self.env.get_action(self.q, state, self.epsilon, True)
                championship.append(action)            
            
            formatted_championship = []
            formatted_championship.append("{}-{}".format(championship[0], championship[-1]))
            for state in formatted_championship:
                action = self.env.get_action(self.q, state, self.epsilon, True)
                winner = action
            print("CHAMPIONSHIP:", formatted_championship)

            print("NCAA CHAMPION:", "['{}']".format(winner))
            print(self.q)
        
    def predict(self):
        """
        After training the agent on the past March Madness results, the Q-Learning agent
        will be able to (hopefully) predict the outcome of a future tournament.
        """
        conferences = {"W": "East", "X": "Midwest", "Y": "South", "Z": "West"}
        #for conf in conferences:
            
            
agent = QAgent(0.2, 0.2, 0.8)
agent.epsilon_greedy_train()

#agent.predict()
