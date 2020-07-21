import pytest


class TestApp:

    @staticmethod
    def test_index_page(mock_get_requests, client):
        response = client.get('/')
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "name 1" in response_data
        assert "desc 4" in response_data

    @staticmethod
    def test_add_item_page(mock_get_requests, client):
        response = client.get('/AddItem')
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "Title" in response_data
        assert "Description" in response_data
        assert "Due date" in response_data

    @staticmethod
    def test_add_item_page_save(mock_post_requests, client):
        response = client.post('/AddItem/Save', data=dict(
            title='Title',
            description='Description'
        ))
        assert response.status_code == 302
        assert len(mock_post_requests) == 1
        assert mock_post_requests[0]['method'] == 'POST'
        assert mock_post_requests[0]['endpoint'] == 'card'
        assert mock_post_requests[0]['params']['name'] == 'Title'
        assert mock_post_requests[0]['params']['desc'] == 'Description'

    @staticmethod
    def test_start_item(mock_post_requests, client):
        response = client.post('/StartItem', data=dict(
            id='1'
        ))
        assert response.status_code == 302
        assert len(mock_post_requests) == 1
        assert mock_post_requests[0]['method'] == 'PUT'
        assert mock_post_requests[0]['endpoint'] == 'cards/1'
        assert mock_post_requests[0]['params']['idList'] == '2' # DOING LIST ID

    @staticmethod
    def test_complete_item(mock_post_requests, client):
        response = client.post('/CompleteItem', data=dict(
            id='1'
        ))
        assert response.status_code == 302
        assert len(mock_post_requests) == 1
        assert mock_post_requests[0]['method'] == 'PUT'
        assert mock_post_requests[0]['endpoint'] == 'cards/1'
        assert mock_post_requests[0]['params']['idList'] == '3' # DONE LIST ID

    @staticmethod
    def test_remove_item(mock_post_requests, client):
        response = client.post('/RemoveItem', data=dict(
            id='1'
        ))
        assert response.status_code == 302
        assert len(mock_post_requests) == 1
        assert mock_post_requests[0]['method'] == 'PUT'
        assert mock_post_requests[0]['endpoint'] == 'cards/1'
        assert mock_post_requests[0]['params']['closed'] == 'true'
