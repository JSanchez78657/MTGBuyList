import requests
import json

params = "unique:prints not:digital"


def get_sets(cards):
    for card in cards:
        prices = card['prices']
        print(card['set'].upper() + ' ' + (prices['usd'] or 'N/A'))


def find_prints(name):
    query = '?q=!' + '\"' + name + '\" ' + params
    request = requests.get('https://api.scryfall.com/cards/search' + query)
    print(request.url)
    get_sets(request.json()['data'])
    return request.json()


find_prints("Ghoulcaller Gisa")
