from typing import Type

from getters import AbstractGetter, SavedFixturesGetter
from parser import AbstractParser, Event
from views import AbstractView, PrintView

default_getter_class: Type[AbstractGetter] = SavedFixturesGetter
default_parser_class: AbstractParser = Event
default_view_class: AbstractView = PrintView


def parse() -> None:
    """
    Parse event's history
    """
    events_data = default_getter_class.get_events()
    events = [
        default_parser_class(
            data=data, previous_data=events_data[i - 1] if i > 0 else None
        )
        for i, data in enumerate(events_data)
    ]
    for event in events:
        default_view_class(messages=event.messages).output_data()


if __name__ == "__main__":
    parse()
