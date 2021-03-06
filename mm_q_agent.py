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
                    self.q[state_action_key] += reward
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
                    second_r_actions.append(action)
                
                round_3 = self.env.get_round_three(second_r_actions)
                print("ROUND3:", round_3)

                third_r_actions = []
                for state in round_3:
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 3)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += reward
                    third_r_actions.append(action)

                round_4 = self.env.get_round_four(third_r_actions)
                print("ROUND4:", round_4)

                fourth_r_actions = []
                for state in round_4:
                    action = self.env.get_action(self.q, state, self.epsilon)
                    reward = self.env.get_reward(action, year, conf, self.data, 4)
                    total_reward += reward
                    state_action_key = "{}-{}".format(state, action)
                    self.q[state_action_key] += reward
                    
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
        
    def predict(self):
        """
        After training the agent on the past March Madness results, the Q-Learning agent
        will be able to (hopefully) predict the outcome of a future tournament.
        """
        conferences = {"W": "East", "X": "Midwest", "Y": "South", "Z": "West"}
        conf_winners = []
        final_four_round = []
        championship_round = []
        champion = []

        for conf in conferences:
            first_round = ["01-16", "02-15", "03-14", "04-13", "05-12", "06-11", "07-10", "08-09"]
            second_round = []
            third_round = []
            fourth_round = []
            
            print("CONFERENCE: {}".format(conferences[conf]))
            round_1_winners = []
            for matchup in first_round:
                winner = self.env.get_action(self.q, matchup, self.epsilon)
                round_1_winners.append(winner)
            print("ROUND1: {}".format(first_round))

            second_round.append("{}-{}".format(round_1_winners[0], round_1_winners[-1]))
            second_round.append("{}-{}".format(round_1_winners[1], round_1_winners[-2]))
            second_round.append("{}-{}".format(round_1_winners[2], round_1_winners[-3]))
            second_round.append("{}-{}".format(round_1_winners[3], round_1_winners[-4]))
            print("PREDICTED ROUND2: {}".format(second_round))

            round_2_winners = []
            for matchup in second_round:
                winner = self.env.get_action(self.q, matchup, self.epsilon)
                round_2_winners.append(winner)

            third_round.append("{}-{}".format(round_2_winners[0], round_2_winners[-1]))
            third_round.append("{}-{}".format(round_2_winners[1], round_2_winners[-2]))
            print("PREDICTED ROUND3: {}".format(third_round))

            round_3_winners = []
            for matchup in third_round:
                winner = self.env.get_action(self.q, matchup, self.epsilon)
                round_3_winners.append(winner)

            fourth_round.append("{}-{}".format(round_3_winners[0], round_3_winners[-1]))
            print("PREDICTED ROUND4: {}".format(fourth_round))
            
            round_4_winner = []
            for matchup in third_round:
                winner = self.env.get_action(self.q, matchup, self.epsilon)
                round_4_winner.append(winner)

            conf_winners.append("{}{}".format(conf, round_4_winner[0]))

        final_four_round.append("{}-{}".format(conf_winners[0], conf_winners[-1]))
        final_four_round.append("{}-{}".format(conf_winners[1], conf_winners[-2]))
        print("PREDICTED FINAL FOUR: {}".format(final_four_round))
        final_four_winners = []
        for matchup in final_four_round:
            action1 = matchup[:3]
            action2 = matchup[4:]
            s_a_key1 = "{}-{}".format(matchup, action1)
            s_a_key2 = "{}-{}".format(matchup, action2)
            if self.q[s_a_key1] >= self.q[s_a_key2]:
                final_four_winners.append(action1)
            else:
                final_four_winners.append(action2)

        championship_round.append("{}-{}".format(final_four_winners[0], final_four_winners[-1]))
        print("PREDICTED CHAMPIONSHIP: {}".format(championship_round))

        for matchup in championship_round:
            action1 = matchup[:3]
            action2 = matchup[4:]
            s_a_key1 = "{}-{}".format(matchup, action1)
            s_a_key2 = "{}-{}".format(matchup, action2)
            if self.q[s_a_key1] >= self.q[s_a_key2]:
                champion.append(action1)
            else:
                champion.append(action2)
        print("PREDICTED NCAA CHAMPION: {}".format(champion))

agent = QAgent(0.1, 0.2, 0.8)
agent.epsilon_greedy_train()
agent.predict()

