import pytest
from unittest import mock
from classes.user import User

user_with_write = User('47484139')


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_index_page(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'


@mock.patch('flask_login.utils._get_user', mock.MagicMock(return_value=user_with_write))
def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    add_another_button = driver.find_element_by_link_text('Add another item')
    add_another_button.click()

    title = driver.find_element_by_name("title")
    description = driver.find_element_by_name("description")
    due_date = driver.find_element_by_name("due_date")

    title.send_keys("Test Title")
    description.send_keys("Test Description")
    due_date.send_keys("07/29/2020")
    save_button = driver.find_element_by_xpath('//button[normalize-space()="Save"]')
    save_button.click()

    start_task_button = driver.find_element_by_xpath(
        '//b[normalize-space()="Test Title"]/../button[normalize-space()="Start task"]')
    start_task_button.click()

    complete_task_button = driver.find_element_by_xpath(
        '//b[normalize-space()="Test Title"]/../button[normalize-space()="Complete task"]')
    complete_task_button.click()

    restart_task_button = driver.find_element_by_xpath(
        '//b[normalize-space()="Test Title"]/../button[normalize-space()="Restart task"]')
    restart_task_button.click()

    second_complete_task_button = driver.find_element_by_xpath(
        '//b[normalize-space()="Test Title"]/../button[normalize-space()="Complete task"]')
    assert second_complete_task_button
