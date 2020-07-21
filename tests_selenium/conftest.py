import pytest
from threading import Thread
import os
import app
from helpers.trello_wrapper import TrelloWrapper
from selenium import webdriver
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    trello_wrapper = TrelloWrapper()
    # Create the new board & update the board id environment variable
    board_id = trello_wrapper.create_board_with_lists("test")
    os.environ['BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    trello_wrapper.delete_board(board_id)
