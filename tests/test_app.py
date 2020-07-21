import pytest


class TestApp:

    @staticmethod
    def test_index_page(client):
        response = client.get('/')
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "name 1" in response_data
        assert "desc 4" in response_data
