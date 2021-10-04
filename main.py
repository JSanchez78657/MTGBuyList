import collections
import time
import requests
import pprint
import pyperclip


class SetGetter:
    def __init__(self, names):
        self.params = " unique:prints not:digital"
        self.common_cards = ['Plains', 'Swamp', 'Island', 'Mountain', 'Forest']
        self.last_call = time.time()
        self.names = self.clean_names(names)

    def get_sets(self, name):
        query = '?q=!"' + name + '"' + self.params
        uri = 'https://api.scryfall.com/cards/search' + query

        elapsed = time.time() - self.last_call
        if elapsed < .1:
            time.sleep(.1 - elapsed)
        self.last_call = time.time()
        request = requests.get(uri)
        if request.status_code != 200:
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

    def get_list(self):
        card_list = collections.defaultdict(list)
        for name in self.names:
            card = self.get_sets(name)
            if card is not None:
                card_list[name].append(card)
        return card_list

    def clean_names(self, names):
        remove = []
        for i in range(len(names)):
            if names[i].startswith('/') or names[i] == '':
                remove.append(i)
            while len(names[i]) > 0 and not names[i][0].isalpha():
                names[i] = names[i][1:]
        for i in reversed(remove):
            names.pop(i)
        names = [x for x in names if x not in self.common_cards]
        for i in range(len(names)):
            if '#!Commander' in names[i]:
                names[i] = names[i][0:-12]
        return names


start = time.time()
getter = SetGetter(pyperclip.paste().split("\r\n"))
pp = pprint.PrettyPrinter()
pp.pprint(getter.get_list())
print("Execution took %s seconds." % (time.time() - start))
