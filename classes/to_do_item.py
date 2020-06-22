from config.trello_config import TODO_LIST_ID, DOING_LIST_ID, DONE_LIST_ID
import dateutil.parser


class Item(object):

    def __init__(self, card):
        self.id = card['id']
        self.title = card['name']
        self.description = card['desc']
        if card['due']:
            date = dateutil.parser.parse(card['due'])
            self.due_date = date.strftime('%d/%m/%Y')
        self.deleted = False

        if card['idList'] == TODO_LIST_ID:
            self.status = 'Not Started'
        elif card['idList'] == DOING_LIST_ID:
            self.status = 'In Progress'
        elif card['idList'] == DONE_LIST_ID:
            self.status = 'Completed'
        else:
            self.deleted = True
