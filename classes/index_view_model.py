from datetime import datetime
from typing import List
from classes.to_do_item import Item


class IndexViewModel:

    def __init__(self, items: List[Item], show_completed: bool):
        self._items = items
        self._show_all_done_items = show_completed

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def show_all_done_items(self) -> bool:
        return self._show_all_done_items

    @property
    def sorted_items(self) -> List[Item]:
        return sorted(self._items, key=lambda item: item.status, reverse=True)

    @property
    def to_do_items(self) -> List[Item]:
        items = sorted(self._items, key=lambda item: item.due_date, reverse=True)
        return [item for item in items if item.status == "To Do"]

    @property
    def doing_items(self) -> List[Item]:
        items = sorted(self._items, key=lambda item: item.due_date, reverse=True)
        return [item for item in items if item.status == "Doing"]

    @property
    def done_items(self) -> List[Item]:
        items = sorted(self._items, key=lambda item: item.due_date, reverse=True)
        return [item for item in items if item.status == "Done"]

    @property
    def recent_done_items(self) -> List[Item]:
        items = sorted(self._items, key=lambda item: item.due_date, reverse=True)
        print(items)
        return [item for item in items if
                item.status == "Done"
                and datetime.date(item.completed_on) == datetime.date(self.today())]

    @staticmethod
    def today():
        return datetime.today().replace(tzinfo=None)
