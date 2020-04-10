"""
ArbitrageBetting2, by Liam Wood-Baker, 2020
This is my second attempt at a program to find arbitrage opportunities. This time, instead of scraping various betting
websites for odds, I will be using the-odds-api, which will get lots of odds from all around the world for me.
"""

import json
import requests

# Keep the key for the-odds-api key secret
api_key = open('api_key.txt').read()
gameObjects = []


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


# Now get the odds for each event in each sport for each agency. 'Sport' being set to 'upcoming' means that the odds
# for all upcoming games will be returned
odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,
    'sport': 'upcoming',
    'region': 'au', # uk | us | eu | au
    'mkt': 'h2h' # h2h | spreads | totals
})
odds_json = json.loads(odds_response.text)
for game in odds_json['data']:
    sport_key = game['sport_key']
    teamA, teamB = game['teams']
    for site in game['sites']:
        bettingAgency = site['site_key']
        oddsA, oddsB = site['odds']['h2h']
        gameObjects.append(Game(bettingAgency=bettingAgency, teamA=teamA, teamB = teamB, oddsA=oddsA, oddsB=oddsB))
