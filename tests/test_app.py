from unittest import mock
import pytest
from classes.user import User
from helpers.mongo_wrapper import MongoWrapper
import mongomock
from datetime import datetime
from classes.index_view_model import IndexViewModel

user_with_write = User('47484139')

todays_date = datetime(2001, 1, 10)
old_date = datetime(2001, 1, 7)


def get_cards():
    cards = []
    for i in range(1, 9):
        card = {
            '_id': '00000000000000000000000' + str(i),
            'name': 'name ' + str(i),
            'desc': 'desc ' + str(i),
            'due': '01/01/2019',
            'deleted': False
        }
        if i < 2:
            card['status'] = 'To Do'
        elif i < 4:
            card['status'] = 'Doing'
        elif i < 6:
            card['status'] = 'Done'
            card['completedOn'] = todays_date
        else:
            card['status'] = 'Done'
            card['completedOn'] = old_date
        cards.append(card)
    return cards


@pytest.fixture(autouse=True)
def mock_db_init(monkeypatch):
    def mock_get_cards(*args, **kwargs):
        cards = mongomock.MongoClient().test.cards
        cards.insert_many(get_cards())
        return cards

    monkeypatch.setattr(MongoWrapper, "_get_cards", mock_get_cards)


@pytest.fixture(autouse=True)
def mock_datetime_today(monkeypatch):
    def datetime_today(*args, **kwargs):
        return todays_date

    monkeypatch.setattr(IndexViewModel, "today", datetime_today)


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    response_data = response.data.decode("utf-8")
    assert "name 1" in response_data
    assert "desc 4" in response_data


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_add_item_page(client):
    response = client.get('/AddItem')
    assert response.status_code == 200
    response_data = response.data.decode("utf-8")
    assert "Title" in response_data
    assert "Description" in response_data
    assert "Due date" in response_data


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_add_item_page_save(client):
    response = client.post('/AddItem/Save', data=dict(
        title='Title',
        description='Description'
    ))
    assert response.status_code == 302


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_start_item(client):
    response = client.post('/StartItem', data=dict(
        id='000000000000000000000001'
    ))
    assert response.status_code == 302


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_complete_item(client):
    response = client.post('/CompleteItem', data=dict(
        id='000000000000000000000001'
    ))
    assert response.status_code == 302


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_remove_item(client):
    response = client.post('/RemoveItem', data=dict(
        id='000000000000000000000001'
    ))
    assert response.status_code == 302
