import pytest


class TestApp:

    @staticmethod
    def test_index_page(driver, test_app):
        driver.get('http://localhost:5000/')
        assert driver.title == 'To-Do App'
