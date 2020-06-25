import dateutil.parser


class Item(object):

    def __init__(self, card, to_do_list, doing_list, done_list):
        self.id = card['id']
        self.title = card['name']
        self.description = card['desc']
        if card['due']:
            date = dateutil.parser.parse(card['due'])
            self.due_date = date.strftime('%d/%m/%Y')
        self.deleted = False

        if card['idList'] == to_do_list['id']:
            self.status = 'Not Started'
        elif card['idList'] == doing_list['id']:
            self.status = 'In Progress'
        elif card['idList'] == done_list['id']:
            self.status = 'Completed'
        else:
            self.deleted = True
