"""
ArbitrageBetting2, by Liam Wood-Baker, 2020
This is my second attempt at a program to find arbitrage opportunities. This time, instead of scraping various betting
websites for odds, I will be using the-odds-api, which will get lots of odds from all around the world for me.
"""

import json
import requests


# These classes and functions are from the original ArbitrageBetting project, with some changes to better suit
# the API we're using
class Game:
    def __init__(self, bettingAgency, teamA, teamB, oddsA, oddsB, ):
        self.bettingAgency = bettingAgency
        self.teamA = teamA
        self.teamB = teamB
        self.oddsA = oddsA
        self.oddsB = oddsB
        self.impliedOddsA = 1 / oddsA
        self.impliedOddsB = 1 / oddsB
        self.gameID = teamA + ' vs ' + teamB


# the combined market margin is the sum of the two implied probabilites.
# if it's < 1, then there is an arbitrage opportunity
def combinedMarketMargin(odds1, odds2):
    return (1 / odds1) + (1 / odds2)


# If there is an arbitrage opportunity, then to calculate the profit for a
# given investment the following formula is used:
#
# Profit = (Investment / combined market margin) – Investment
def profit(investment, combinedMarketMargin):
    return (investment / combinedMarketMargin) - investment


# To calculate how much to stake on each side of the arbitrage bet, the following formula is used:
#
# Individual bets = (Investment x Individual implied odds) / combined market margin
def individualBet(investment, individualImpliedOdds, combinedMarketMargin):
    return (investment * individualImpliedOdds) / combinedMarketMargin

# Keep the API key secret
api_key = open('api_key.txt').read()

# First get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': api_key})
sports_json = json.loads(sports_response.text)
sports_keys = [dictionary['key'] for dictionary in sports_json['data']]  # all the currently available sports

# Now get the odds for each event in each sport for each agency



