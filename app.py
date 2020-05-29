from flask import Flask, render_template, request, redirect, url_for
from session_items import get_items, add_item
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/AddItem')
def addItem():
    return render_template('addItem.html')

@app.route('/AddItem/Save', methods=['POST'])
def addItemSave():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

if __name__ == '__main__':
    app.run()
