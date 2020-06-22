from flask import Flask, render_template, request, redirect, url_for
from session_items import get_items, get_item, add_item, save_item, delete_item

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/')
def index():
    items = get_items()
    sorted_items = sorted(items, key=lambda item: item['status'], reverse=True)
    return render_template('index.html', items=sorted_items)


@app.route('/AddItem')
def add_item_page():
    return render_template('addItem.html')


@app.route('/AddItem/Save', methods=['POST'])
def add_item_save():
    title = request.form.get('title')
    if not title:
        return redirect('/AddItem')
    add_item(title)
    return redirect('/')


@app.route('/CompleteItem', methods=['POST'])
def complete_item():
    item_id = request.form.get('id')
    if not item_id:
        return redirect('/AddItem')
    item = get_item(item_id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect('/')


@app.route('/RemoveItem', methods=['POST'])
def remove_item():
    item_id = request.form.get('id')
    if not item_id:
        return redirect('/AddItem')
    delete_item(item_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
