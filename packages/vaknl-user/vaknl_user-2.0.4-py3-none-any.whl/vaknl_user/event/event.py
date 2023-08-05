"""Event data classes.

Event dataclasses from website clickstream events.

Created: 2020-03-0? (Merijn)
Updated: 2020-07-11 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, InitVar, field, asdict
from typing import List
import operator


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_user import event


# ----------------------------------------------------------------------------------------------------------------------
# Event parent dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Event:
    """Event super class."""
    event_id: str
    timestamp: int
    dmp_session_id: str
    event_value: InitVar[dict] = None

    def __post_init__(self, event_value: dict):
        if event_value:
            # Fill event object with data from event_value_json. Function should be overwritten in child if used.
            self._fill_event_from_event_value(event_value)
        self._force_fields_not_none()

    def _fill_event_from_event_value(self, event_value: dict):
        """Dummy function. Should be overwritten in child dataclass when used."""
        pass

    def _raise_error_if_fields_are_none(self, fields: list):
        """Raises error if given fields are None."""
        is_none = [item for item in fields if getattr(self, item) is None]
        is_none_str = "['" + "', '".join(is_none) + "']"
        assert not is_none, f'The following fields should be declared: {is_none_str}.'

    def _force_fields_not_none(self):
        """Dummy function. Should be overwritten in child dataclass when used."""
        pass

    @staticmethod
    def _custom_factory_dict(data: dict) -> dict:
        """Remove `dummy` attribute in dict. The dummy field is used in otherwise empty parent dataclasses to avoid
        inheritance problems."""
        return dict(x for x in data if x[0] != "dummy")

    def to_dict(self):
        """Write attributes to dictionary."""
        return asdict(self, dict_factory=self._custom_factory_dict)


# ----------------------------------------------------------------------------------------------------------------------
# Events dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Events:
    """Class for multiple events together, with ordering method."""
    event_list: List[Event] = field(default_factory=list)

    def sort_by_timestamp_ascending(self):
        """Sorts events ascending by timestamp."""
        self.event_list = sorted(self.event_list, key=operator.attrgetter('timestamp'))

    def add_event(self, e: Event):
        """Add single event."""
        assert isinstance(e, Event), 'The provided `e` is not an `Event` instance.'
        self.event_list.append(e)

    def add_raw_event(self, clickstream_event_data: dict):
        """Add single event from data of a clickstream event."""
        e = event.create_event(clickstream_event_data)
        if e is not None:
            self.event_list.append(e)

    def add_raw_events(self, clickstream_event_list: list):
        """Add multiple events from list of clickstream events."""
        for item in clickstream_event_list:
            try:
                self.add_raw_event(item)
            except Exception as expt:
                # Broad except statement is necessary to avoid that an error for a single event breaks the entire
                # process.
                print(expt)

    def merge(self, ee):
        """Merge second Events object into self."""
        assert isinstance(ee, self.__class__), f'`ee` should be a {self.__class__} instance.'
        self.event_list += ee.event_list
