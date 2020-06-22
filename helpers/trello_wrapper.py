import os
import requests

from config.trello_config import BOARD_ID, TODO_LIST_ID, DOING_LIST_ID, DONE_LIST_ID
from classes.to_do_item import Item

trelloUrl = 'https://api.trello.com'


def get_items():
    cards = __send_trello_request('GET', f'/1/boards/{BOARD_ID}/cards', {}).json()
    items = []
    for card in cards:
        item = Item(card)
        if not item.deleted:
            items.append(item)

    return items


def create_new_item(title, description, due_date):
    query = {
        'idList': TODO_LIST_ID,
        'name': title,
        'desc': description,
        'due': due_date
    }
    return __send_trello_request('POST', '/1/card', query)


def move_item_to_doing(item_id):
    query = {
        'idList': DOING_LIST_ID
    }
    return __send_trello_request('PUT', f'/1/cards/{item_id}', query)


def move_item_to_done(item_id):
    query = {
        'idList': DONE_LIST_ID
    }
    return __send_trello_request('PUT', f'/1/cards/{item_id}', query)


def archive_item(item_id):
    query = {
        'closed': 'true'
    }
    return __send_trello_request('PUT', f'/1/cards/{item_id}', query)


def __send_trello_request(method, suffix, query):
    query['key'] = os.getenv("TRELLO_KEY")
    query['token'] = os.getenv("TRELLO_TOKEN")

    headers = {
        'Accept': 'application/json'
    }

    return requests.request(method, trelloUrl + suffix, params=query, headers=headers)
