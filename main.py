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
arbitrageObjects = []


# Some classes and functions are from the original ArbitrageBetting project, with some changes to better suit
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


class PossibleArbitrage:
    def __init__(self, teamA, teamB, oddsA, oddsB, agencyA, agencyB):
        self.teamA = teamA
        self.teamB = teamB
        self.oddsA = oddsA
        self.oddsB = oddsB
        self.agencyA = agencyA
        self.agencyB = agencyB
        self.gameID = teamA + ' vs ' + teamB
        self.CMM = combinedMarketMargin(oddsA, oddsB)


# def createPossibleArbitrages(game_object_1, game_object_2):
#     # the teamA and teamB for the two game objects should be the same
#     agency1 = game_object_1.bettingAgency
#     agency2 = game_object_2.bettingAgency
#     teamA = game_object_1.teamA
#     teamB = game_object_1.teamB
#     odds1 = [game_object_1.oddsA, game_object_1.oddsB]
#     odds2 = [game_object_2.oddsA, game_object_2.oddsB]
#     # append A to B
#     arbitrageObjects.append(PossibleArbitrage(teamA=teamA, teamB=teamB,
#                                               oddsA=odds1[0]), oddsB=odds2[1],
#                             agencyA=agency1, agencyB=agency2)
#     # append B to A
#     arbitrageObjects.append(PossibleArbitrage(teamA=teamA, teamB=teamB,
#                                               oddsA=odds2[0]), oddsB=odds1[1],
#                             agencyA=agency2, agencyB=agency1)


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
    'region': 'au',  # uk | us | eu | au
    'mkt': 'h2h'  # h2h | spreads | totals
})
odds_json = json.loads(odds_response.text)
for game in odds_json['data']:
    sport_key = game['sport_key']
    teamA, teamB = game['teams']
    for site in game['sites']:
        bettingAgency = site['site_key']
        oddsA, oddsB = site['odds']['h2h']
        gameObjects.append(Game(bettingAgency=bettingAgency, teamA=teamA, teamB=teamB, oddsA=oddsA, oddsB=oddsB))
# gameObjects now has an object for each set of odds for each game in it


# now we need to find any arbitrage opportunities that might exist
gameIDs = {ID.gameID for ID in gameObjects}
for ID in gameIDs:
    # all the games with the same gameID
    relevant_games = filter(lambda x: x.gameID == ID, gameObjects)
    for game1 in relevant_games:
        for game2 in relevant_games:
            arbitrageObjects.append(PossibleArbitrage(teamA=game1.teamA, teamB=game2.teamB,
                                                      oddsA=game1.oddsA, oddsB=game2.oddsB,
                                                      agencyA=game1.bettingAgency, agencyB=game2.bettingAgency))

# sort for the best arbitrage opportunities
arbitrageObjects.sort(key=lambda x: x.CMM)

# output what we've found
for arbitrage_object in arbitrageObjects:
    implied_oddsA = 1 / arbitrage_object.oddsA
    implied_oddsB = 1 / arbitrage_object.oddsB
    CMM = arbitrage_object.CMM
    print('For ' + arbitrage_object.gameID +
          '\na CMM of ' + str(arbitrage_object.CMM) +
          '\ncan be achieved through ' + arbitrage_object.agencyA + ' and ' + arbitrage_object.agencyB + '.' +
          '(' + str(arbitrage_object.oddsA) + ' to ' + str(arbitrage_object.oddsB) + ')' +
          '\nBet ' + str(individualBet(investment=100, individualImpliedOdds=implied_oddsA,
                                       combinedMarketMargin=CMM)) + '% on ' + arbitrage_object.teamA
          + ', and ' + str(individualBet(investment=100, individualImpliedOdds=implied_oddsB,
                                         combinedMarketMargin=CMM)) + '% on ' + arbitrage_object.teamB
          + '.'
          + '\nProfit: ' + str(profit(investment=100, combinedMarketMargin=CMM)) + '%.'
          + '\n\n'
          )
