import pytest
import requests
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
from app import create_app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


class MockListsResponse:
    @staticmethod
    def json():
        return [{'id': '1', 'name': 'To Do'}, {'id': '2', 'name': 'Doing'}, {'id': '3', 'name': 'Done'}]


class MockCardsResponse:
    @staticmethod
    def json():
        cards = []
        for i in range(1, 9):
            card = {
                'id': str(i),
                'name': 'name ' + str(i),
                'desc': 'desc ' + str(i),
                'due': (datetime.now() + timedelta(days=10)).isoformat(),
                'idList': '0',
                'dateLastActivity': None
            }
            if i < 2:
                card['idList'] = '1'
            elif i < 4:
                card['idList'] = '2'
            elif i < 6:
                card['idList'] = '3'
                card['dateLastActivity'] = datetime.now().isoformat()
            else:
                card['idList'] = '3'
                card['dateLastActivity'] = (datetime.now() + timedelta(days=-3)).isoformat()
            cards.append(card)
        return cards


class MockPostResponse:
    @staticmethod
    def json():
        return ""


@pytest.fixture()
def mock_get_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        if args[1] == 'https://api.trello.com/1/boards/board-id/lists':
            return MockListsResponse
        elif args[1] == 'https://api.trello.com/1/boards/board-id/cards':
            return MockCardsResponse

    monkeypatch.setattr(requests, "request", mock_get)


@pytest.fixture()
def mock_post_requests(monkeypatch):
    calls = []

    def mock_post(*args, **kwargs):
        if args[1] == 'https://api.trello.com/1/boards/board-id/lists':
            return MockListsResponse
        elif args[1] == 'https://api.trello.com/1/boards/board-id/cards':
            return MockCardsResponse
        elif args[1] == 'https://api.trello.com/1/card':
            calls.append(dict(
                method="POST",
                endpoint="card",
                params=kwargs["params"]
            ))
            return MockPostResponse
        elif args[1] == 'https://api.trello.com/1/cards/1':
            calls.append(dict(
                method="PUT",
                endpoint="cards/1",
                params=kwargs["params"]
            ))
            return MockPostResponse

    monkeypatch.setattr(requests, "request", mock_post)
    return calls
