import pytest

from datetime import datetime, timedelta
from classes.index_view_model import IndexViewModel
from classes.to_do_item import Item


@pytest.fixture()
def index_view_model():
    to_do_list = {'id': '1'}
    doing_list = {'id': '2'}
    done_list = {'id': '3'}
    items = []
    for i in range(1, 9):
        card = {
            'id': str(i),
            'name': 'name ' + str(i),
            'desc': 'desc ' + str(i),
            'due': (datetime.now() + timedelta(days=10)).isoformat(),
            'idList': '0',
            'dateLastActivity' : None
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

        item = Item(card, to_do_list, doing_list, done_list)
        items.append(item)

    return IndexViewModel(items, True)


class TestIndexViewModel:
    @staticmethod
    def test_to_do_items_is_right_length(index_view_model: IndexViewModel):
        assert len(index_view_model.to_do_items) == 1

    @staticmethod
    def test_to_do_items_are_right_status(index_view_model: IndexViewModel):
        assert all(item.status == 'Not Started' for item in index_view_model.to_do_items)

    @staticmethod
    def test_doing_items_is_right_length(index_view_model: IndexViewModel):
        assert len(index_view_model.doing_items) == 2

    @staticmethod
    def test_doing_items_are_right_status(index_view_model: IndexViewModel):
        assert all(item.status == 'In Progress' for item in index_view_model.doing_items)

    @staticmethod
    def test_done_items_is_right_length(index_view_model: IndexViewModel):
        assert len(index_view_model.done_items) == 5

    @staticmethod
    def test_done_items_are_right_status(index_view_model: IndexViewModel):
        assert all(item.status == 'Completed' for item in index_view_model.done_items)

    @staticmethod
    def test_show_all_done_items_is_right_bool():
        view_model_a = IndexViewModel([], True)
        view_model_b = IndexViewModel([], False)
        assert view_model_a.show_all_done_items
        assert not view_model_b.show_all_done_items

    @staticmethod
    def test_recently_done_items_is_right_length(index_view_model: IndexViewModel):
        assert len(index_view_model.recent_done_items) == 2

    @staticmethod
    def test_recently_done_items_are_right_status(index_view_model: IndexViewModel):
        assert all(item.status == 'Completed' for item in index_view_model.recent_done_items)

    @staticmethod
    def test_older_done_items_is_right_length(index_view_model: IndexViewModel):
        assert len(index_view_model.older_done_items) == 3

    @staticmethod
    def test_older_done_items_are_right_status(index_view_model: IndexViewModel):
        assert all(item.status == 'Completed' for item in index_view_model.older_done_items)
