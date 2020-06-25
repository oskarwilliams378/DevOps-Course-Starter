from flask import Flask, render_template, request, redirect, url_for
from helpers.trello_wrapper import TrelloWrapper

trelloUrl = 'https://api.trello.com'
baseTrelloQuery = ''

app = Flask(__name__)
app.config.from_object('flask_config.Config')
trello = TrelloWrapper()


@app.route('/')
def index():
    items = trello.get_items()
    sorted_items = sorted(items, key=lambda item: item.status, reverse=True)
    return render_template('index.html', items=sorted_items)


@app.route('/AddItem')
def add_item_page():
    return render_template('addItem.html')


@app.route('/AddItem/Save', methods=['POST'])
def add_item_save():
    title = request.form.get('title')
    if not title:
        return redirect('/AddItem')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    trello.create_new_item(title, description, due_date)
    return redirect('/')


@app.route('/StartItem', methods=['POST'])
def start_item():
    item_id = request.form.get('id')
    if not item_id:
        return redirect('/')
    trello.move_item_to_doing(item_id)
    return redirect('/')


@app.route('/CompleteItem', methods=['POST'])
def complete_item():
    item_id = request.form.get('id')
    if not item_id:
        return redirect('/')
    trello.move_item_to_done(item_id)
    return redirect('/')


@app.route('/RemoveItem', methods=['POST'])
def remove_item():
    item_id = request.form.get('id')
    if not item_id:
        return redirect('/')
    trello.archive_item(item_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
