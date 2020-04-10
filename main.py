"""
ArbitrageBetting2, by Liam Wood-Baker, 2020
This is my second attempt at a program to find arbitrage opportunities. This time, instead of scraping various betting
websites for odds, I will be using the-odds-api, which will get lots of odds from all around the world for me.
"""

import json
import requests




# Keep the API key secret
api_key = open('api_key.txt').read()

# First get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': api_key})
sports_json = json.loads(sports_response.text)
sports_keys = [dictionary['key'] for dictionary in sports_json['data']]  # all the currently available sports

# Now get the odds for each event in each sport for each agency



