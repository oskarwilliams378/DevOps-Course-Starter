from dateutil import parser
from datetime import datetime


class Item(object):

    def __init__(self, card, to_do_list, doing_list, done_list):
        self.id = card['id']
        self.title = card['name']
        self.description = card['desc']
        if card['due']:
            date = parser.isoparse(card['due']).replace(tzinfo=None)
            self.due_date = datetime.date(date)
            self.due_date_string = date.strftime('%d/%m/%Y')
        else:
            self.due_date = datetime.date(datetime.today().replace(tzinfo=None))
        self.deleted = False
        if card['dateLastActivity']:
            date = parser.isoparse(card['dateLastActivity']).replace(tzinfo=None)
            self.completed_on = datetime.date(date)
            self.completed_on_string = date.strftime('%d/%m/%Y')

        if card['idList'] == to_do_list['id']:
            self.status = 'Not Started'
        elif card['idList'] == doing_list['id']:
            self.status = 'In Progress'
        elif card['idList'] == done_list['id']:
            self.status = 'Completed'
        else:
            self.deleted = True
