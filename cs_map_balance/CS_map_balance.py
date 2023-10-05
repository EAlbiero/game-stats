import random as rd
import numpy as np
import matplotlib.pyplot as plt

def main():

    N = 1000
    ROUNDS = 24
    
    percentage_games_won = []
    win_rates = np.linspace(0, 1, 100, endpoint=False)[1:]
    for win_rate in win_rates:
        percentage_games_won.append(estimateAverageRoundsWon(win_rate, ROUNDS, N, overtime_rounds=2))

    plt.scatter(win_rates, percentage_games_won)
    plt.plot([0, 1], [0.5, 0.5], alpha = 0.5, color = "red")
    plt.title("Probability of winning a game based on map balance")
    plt.xlabel("Probability of CT-Side winning the round")
    plt.ylabel("Percentage of games won starting out as a CT")
    plt.show()
    

def playMap(win_rate: float, TOTAL_ROUNDS: int, use_overtime: bool, overtime_rounds: int):
    """
    Float ---> Int
    Simulates a 26 rounds match. For each round the CT team has a win_rate probability to win the round.
    The team we focus on starts and halfway through the match they switch to the T side and now have
    a probability of 1-win_rate to win each round. The function returns the number of rounds won when
    the map ended.
    """
    current_round = 1
    round_wins = 0
    halfway_mark = TOTAL_ROUNDS//2
    map_has_ended = False

    # Checks if either team has won the map by scoring 13 points
    while map_has_ended == False:
        r = rd.random()
        if (current_round <= halfway_mark and r < win_rate) or (current_round > halfway_mark and r > win_rate):
            round_wins += 1

        if round_wins > halfway_mark or current_round - round_wins > halfway_mark:
            break
        current_round +=1
        if current_round > TOTAL_ROUNDS and round_wins == halfway_mark and use_overtime == True:
            TOTAL_ROUNDS = overtime_rounds
            halfway_mark = TOTAL_ROUNDS//2
            current_round = 1
            win_rate = 1-win_rate
            round_wins = 0
            
        map_has_ended = (current_round > TOTAL_ROUNDS)

    return round_wins, current_round - round_wins

def estimateAverageRoundsWon(win_rate: float, rounds: int,  N: int, use_overtime = True, overtime_rounds = 6):
    wins = 0
    for i in range(N):
        w, l = playMap(win_rate, rounds, use_overtime, overtime_rounds)
        
        if w > l:
            wins += 1
    return wins/N






main()