import collections
import time
import requests
import pprint
import pyperclip

params = "unique:prints not:digital"
common_cards = ['Plains', 'Swamp', 'Island', 'Mountain', 'Forest']


def get_sets(name):
    query = '?q=!' + '\"' + name + '\" ' + params
    request = requests.get('https://api.scryfall.com/cards/search' + query)
    if request.status_code == 404:
        return None
    card_sets = collections.defaultdict(list)
    for printing in request.json()['data']:
        prices = printing['prices']
        print_set = collections.defaultdict(list)
        for price in prices:
            if prices[price] is not None:
                print_set[price.upper()] = prices[price]
        card_sets[printing['set'].upper()] = print_set
    return card_sets


def get_list(names):
    card_list = collections.defaultdict(list)
    for name in names:
        # print(name + '...')
        if name not in common_cards:
            card = get_sets(name)
            if card is not None:
                card_list[name].append(card)
        # print(' done!')
        time.sleep(0.1)
    return card_list


name_list = pyperclip.paste().split("\r\n")
for i in range(len(name_list)):
    while len(name_list[i]) > 0 and not name_list[i][0].isalpha():
        name_list[i] = name_list[i][1:]
pp = pprint.PrettyPrinter()
pp.pprint(get_list(name_list))
