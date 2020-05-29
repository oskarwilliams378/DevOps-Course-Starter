from flask import Flask, render_template, request, redirect, url_for
from session_items import get_items, get_item, add_item, save_item, remove_item

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
    print(title)
    add_item(title)
    return redirect('/')


@app.route('/EditItem', methods=['POST'])
def edit_item():
    complete_id = request.form.get('complete_id')
    remove_id = request.form.get('remove_id')
    print(remove_id)
    if complete_id:
        item = get_item(complete_id)
        item['status'] = 'Completed'
        save_item(item)
    elif remove_id:
        remove_item(remove_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
