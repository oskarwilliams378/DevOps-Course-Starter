import os
import requests
from typing import List
from classes.to_do_item import Item


class TrelloWrapper:
    def __init__(self):
        self.__board_id = os.getenv("BOARD_ID")
        self.query = {
            'key': os.getenv("TRELLO_KEY"),
            'token': os.getenv("TRELLO_TOKEN")
        }
        lists = self.get_lists()
        self.__to_do_list = next(list for list in lists if list['name'] == "To Do")
        self.__doing_list = next(list for list in lists if list['name'] == "Doing")
        self.__done_list = next(list for list in lists if list['name'] == "Done")

    def get_items(self) -> List[Item]:
        cards = self.__send_trello_request('GET', f'/boards/{self.__board_id}/cards').json()
        items = []
        for card in cards:
            item = Item(card, self.__to_do_list, self.__doing_list, self.__done_list)
            if not item.deleted:
                items.append(item)

        return items

    def get_lists(self):
        return self.__send_trello_request('GET', f'/boards/{self.__board_id}/lists').json()

    def create_new_item(self, title: str, description: str, due_date):
        self.query['idList'] = self.__to_do_list['id']
        self.query['name'] = title
        self.query['desc'] = description
        self.query['due'] = due_date

        return self.__send_trello_request('POST', '/card')

    def move_item_to_doing(self, item_id: int):
        self.query['idList'] = self.__doing_list['id']

        return self.__send_trello_request('PUT', f'/cards/{item_id}')

    def move_item_to_done(self, item_id: int):
        self.query['idList'] = self.__done_list['id']

        return self.__send_trello_request('PUT', f'/cards/{item_id}')

    def archive_item(self, item_id: int):
        self.query['closed'] = 'true'
        return self.__send_trello_request('PUT', f'/cards/{item_id}')

    def create_list(self, name: str):
        self.query['name'] = name
        self.query['idBoard'] = self.__board_id
        return self.__send_trello_request('POST', f'/lists').json()

    def create_board(self, name: str):
        self.query['name'] = name
        return self.__send_trello_request('POST', f'/boards').json()['id']

    def create_board_with_lists(self, name: str):
        self.__board_id = self.create_board(name)
        self.create_list('To Do')
        self.create_list('Doing')
        self.create_list('Done')
        return self.__board_id

    def delete_board(self, board_id: str):
        self.__send_trello_request('DELETE', f'/boards/{self.__board_id}')
        return

    def __send_trello_request(self, method: str, suffix: str):
        trello_url = 'https://api.trello.com/1'
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request(method, trello_url + suffix, params=self.query, headers=headers)
        return response
