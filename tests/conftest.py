import pytest
from dotenv import find_dotenv, load_dotenv
import mongomock
from helpers.mongo_wrapper import MongoWrapper
from app import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(MongoWrapper, "_create_client", mongomock.MongoClient)
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()
    with test_app.test_client() as client:
        yield client
