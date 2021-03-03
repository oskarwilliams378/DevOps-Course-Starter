from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user
from classes.index_view_model import IndexViewModel
from oauthlib.oauth2 import WebApplicationClient
from classes.user import User
from helpers.mongo_wrapper import MongoWrapper
import requests
import os
import functools


def is_writer(user):
    return user.id == '47484139'


def writer_only(func):
    @functools.wraps(func)
    def wrapper():
        if not is_writer(current_user):
            return redirect('/')
        return func()
    return wrapper


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')
    item_store = MongoWrapper(os.environ['DEFAULT_DATABASE'])

    login_manager = LoginManager()
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    authorization_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    oauth_client = WebApplicationClient(client_id)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(oauth_client.prepare_request_uri(authorization_url))

    @login_manager.user_loader
    def load_user(user_id):
        if oauth_client.access_token is None:
            return None
        login_user(User(user_id))
        return User(user_id)

    @app.route('/login/callback')
    def login():
        response = requests.post(
            oauth_client.prepare_request_uri(
                access_token_url,
                client_secret=client_secret,
                code=request.args.get('code')))
        oauth_client.parse_request_body_response(response.text)
        parsed_uri = oauth_client.add_token('https://api.github.com/user')
        user = requests.get(parsed_uri[0], headers=parsed_uri[1]).json()
        load_user(user['id'])
        return redirect('/')

    @app.route('/')
    @login_required
    def index():
        show_completed = request.args.get('show_completed') == 'True'
        items = item_store.get_items()
        view_model = IndexViewModel(items, show_completed, is_writer(current_user))
        return render_template('index.html', view_model=view_model)

    @app.route('/AddItem')
    @login_required
    @writer_only
    def add_item_page():
        return render_template('addItem.html')

    @app.route('/AddItem/Save', methods=['POST'])
    @login_required
    @writer_only
    def add_item_save():
        title = request.form.get('title')
        if not title:
            return redirect('/AddItem')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        item_store.create_new_item(title, description, due_date)
        return redirect('/')

    @app.route('/StartItem', methods=['POST'])
    @login_required
    @writer_only
    def start_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.move_item_to_doing(item_id)
        return redirect('/')

    @app.route('/CompleteItem', methods=['POST'])
    @login_required
    @writer_only
    def complete_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.move_item_to_done(item_id)
        return redirect('/')

    @app.route('/RemoveItem', methods=['POST'])
    @login_required
    @writer_only
    def remove_item():
        item_id = request.form.get('id')
        if not item_id:
            return redirect('/')
        item_store.archive_item(item_id)
        return redirect('/')

    @app.route('/ShowCompleted', methods=['POST'])
    @login_required
    def show_all_done_items():
        show_completed = request.form.get('show_completed') == 'False'
        return redirect('/?show_completed=' + str(show_completed))

    if __name__ == '__main__':
        app.run()

    return app
