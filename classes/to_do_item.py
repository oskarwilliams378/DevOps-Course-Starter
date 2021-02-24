from datetime import datetime


class Item(object):
    def __init__(self, card):
        self.id = card['_id']
        self.title = card['name']
        self.description = card['desc']
        self.status = card['status']
        self.deleted = card['deleted']

        if card['due'] != '':
            self.due_date_string = datetime.strptime(card['due'], '%m/%d/%Y').strftime('%d/%m/%Y')
            self.due_date = datetime.date(datetime.strptime(self.due_date_string, '%d/%m/%Y'))
        else:
            self.due_date = datetime.date(datetime.today())

        if self.status == "Done":
            self.completed_on = card['completedOn']
            self.completed_on_string = card['completedOn'].strftime('%d/%m/%Y')
