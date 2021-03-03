import pytest
import os
from threading import Thread
import app
from helpers.mongo_wrapper import MongoWrapper
from selenium import webdriver
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # construct the new application
    mongo_db = MongoWrapper.create_database("SeleniumTest")
    os.environ['DEFAULT_DATABASE'] = "SeleniumTest"
    application = app.create_app()
    application.config.update(dict(LOGIN_DISABLED=True))
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    mongo_db.drop_database()
