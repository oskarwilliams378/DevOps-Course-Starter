from config.trello_config import TODO_ID, DOING_ID, DONE_ID


class Item(object):

    def __init__(self, card):
        self.id = card['id']
        self.title = card['name']
        self.description = card['desc']
        self.deleted = False

        if card['idList'] == TODO_ID:
            self.status = 'Not Started'
        elif card['idList'] == DOING_ID:
            self.status = 'In Progress'
        elif card['idList'] == DONE_ID:
            self.status = 'Completed'
        else:
            self.deleted = True
