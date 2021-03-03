import pytest
from datetime import datetime
from classes.index_view_model import IndexViewModel
from classes.to_do_item import Item

todays_date = datetime(2001, 1, 10)
old_date = datetime(2001, 1, 7)


@pytest.fixture()
def index_view_model():
    items = []
    for i in range(1, 9):
        card = {
            '_id': str(i),
            'name': 'name ' + str(i),
            'desc': 'desc ' + str(i),
            'due': '01/01/2019',
            'idList': '0',
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

        item = Item(card)
        items.append(item)

    return IndexViewModel(items, True, True)


@pytest.fixture(autouse=True)
def mock_datetime_today(monkeypatch):
    def datetime_today(*args, **kwargs):
        return todays_date

    monkeypatch.setattr(IndexViewModel, "today", datetime_today)


def test_to_do_items_is_right_length(index_view_model: IndexViewModel):
    assert len(index_view_model.to_do_items) == 1


def test_to_do_items_are_right_status(index_view_model: IndexViewModel):
    assert all(item.status == 'To Do' for item in index_view_model.to_do_items)


def test_doing_items_is_right_length(index_view_model: IndexViewModel):
    assert len(index_view_model.doing_items) == 2


def test_doing_items_are_right_status(index_view_model: IndexViewModel):
    assert all(item.status == 'Doing' for item in index_view_model.doing_items)


def test_done_items_is_right_length(index_view_model: IndexViewModel):
    assert len(index_view_model.done_items) == 5


def test_done_items_are_right_status(index_view_model: IndexViewModel):
    assert all(item.status == 'Done' for item in index_view_model.done_items)


def test_show_all_done_items_is_right_bool():
    view_model_a = IndexViewModel([], True, True)
    view_model_b = IndexViewModel([], False, True)
    assert view_model_a.show_all_done_items
    assert not view_model_b.show_all_done_items


def test_recently_done_items_is_right_length(index_view_model: IndexViewModel):
    assert len(index_view_model.recent_done_items) == 2


def test_recently_done_items_are_right_status(index_view_model: IndexViewModel):
    assert all(item.status == 'Done' for item in index_view_model.recent_done_items)
