import collections
import time
import requests
import pprint
import pyperclip
from tkinter import *
from tkinter import ttk

common_cards = ['Plains', 'Swamp', 'Island', 'Mountain', 'Forest']
params = " unique:prints not:digital"


def get_sets(name, last_call):
    query = '?q=!"' + name + '"' + params
    uri = 'https://api.scryfall.com/cards/search' + query
    if last_call is not None:
        elapsed = time.time() - last_call
        if elapsed < .1:
            time.sleep(.1 - elapsed)
    request_time = time.time()
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
    return card_sets, request_time


def clean_names(names):
    remove = []
    for i in range(len(names)):
        if names[i].startswith('/') or names[i] == '':
            remove.append(i)
        while len(names[i]) > 0 and not names[i][0].isalpha():
            names[i] = names[i][1:]
    for i in reversed(remove):
        names.pop(i)
    names = [x for x in names if x not in common_cards]
    for i in range(len(names)):
        if '#!Commander' in names[i]:
            names[i] = names[i][0:-12]
    return names


def get_list(raw):
    card_list = collections.defaultdict(list)
    names = clean_names(raw.split('\r\n'))
    last_call = None
    for name in names:
        card, last_call = get_sets(name, last_call)
        if card is not None:
            card_list[name].append(card)
    pprint.pprint(card_list, indent=4)
    return card_list


def paste(textbox):
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', pyperclip.paste())


# start = time.time()
# big_list = get_list(pyperclip.paste().split("\r\n"))
# pp = pprint.PrettyPrinter()
# pp.pprint(big_list)
# print("Execution took %s seconds." % (time.time() - start))
window = Tk()
root_frame = ttk.Frame(window, padding=10)
root_frame.grid()
card_textbox = Text(root_frame, width=40, height=10)
card_textbox.grid(row=0, column=0)
button_frame = ttk.Frame(root_frame)
button_frame.grid(row=0, column=1)
search_button = ttk.Button(
    button_frame,
    text="Search",
    command=lambda: get_list(card_textbox.get('1.0', 'end-1c'))
).grid(row=0, column=0)
clipboard_button = ttk.Button(
    button_frame,
    text="Copy from Clipboard",
    command=lambda: paste(card_textbox)
).grid(row=1, column=0)
window.mainloop()
