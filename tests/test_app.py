import pytest


class TestApp:

    @staticmethod
    def test_index_page(monkeypatch_fixture, client):
        response = client.get('/')
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "name 1" in response_data
        assert "desc 4" in response_data

    @staticmethod
    def test_add_item_page(monkeypatch_fixture, client):
        response = client.get('/AddItem')
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "Title" in response_data
        assert "Description" in response_data
        assert "Due date" in response_data
