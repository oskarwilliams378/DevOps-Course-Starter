from flask import Flask, render_template, request, redirect
from classes.index_view_model import IndexViewModel
from helpers.mongo_wrapper import MongoWrapper
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')
    item_store = MongoWrapper(os.environ['DEFAULT_DATABASE'])

    @app.route('/')
    def index():
        show_completed = request.args.get('show_completed') == 'True'
        items = item_store.get_items()
        view_model = IndexViewModel(items, show_completed)
        return render_template('index.html', view_model=view_model)

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
        item_store.create_new_item(title, description, due_date)
        return redirect('/')

    @app.route('/StartItem', methods=['POST'])
    def start_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.move_item_to_doing(item_id)
        return redirect('/')

    @app.route('/CompleteItem', methods=['POST'])
    def complete_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.move_item_to_done(item_id)
        return redirect('/')

    @app.route('/RemoveItem', methods=['POST'])
    def remove_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.archive_item(item_id)
        return redirect('/')

    @app.route('/ShowCompleted', methods=['POST'])
    def show_all_done_items():
        show_completed = request.form.get('show_completed') == 'False'
        return redirect('/?show_completed=' + str(show_completed))

    if __name__ == '__main__':
        app.run()

    return app
