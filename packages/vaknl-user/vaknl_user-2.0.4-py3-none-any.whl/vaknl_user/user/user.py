"""User dataclass.

User class created from firestore website clickstream data.

Created: 2020-03-0? (Merijn)
Updated: 2020-07-17 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field, asdict
from typing import Dict, List
from dacite import from_dict


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_user.user import utils
from vaknl_user.user.statistics import Statistics
from vaknl_user import event
from vaknl_NBC import NBC


# ----------------------------------------------------------------------------------------------------------------------
# User dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class User:
    """User dataclass for dmp_users."""
    dmp_user_id: str
    statistics: Statistics = field(default_factory=Statistics)

    def __post_init__(self):
        self.validate()

    def add_event(self, e: event.event.Event, nbc_api: NBC = None):
        """Adds single event from an `Event` object.

        Args:
            e: `Event` instance.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        self.statistics.add_event(e, nbc_api)

    def add_events(self, ee: event.event.Events, nbc_api: NBC = None):
        """Adds multiple events represented as an `Events` object.

        Args:
            ee: `Events` instance that contains a list of `Event` instances.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        self.statistics.add_events(ee, nbc_api)

    def add_raw_event(self, raw_event: dict, nbc_api: NBC = None):
        """Adds single raw clickstream event.

        Args:
            raw_event: Raw clickstream event.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        e = event.create_event(raw_event)
        self.add_event(e, nbc_api)

    def add_raw_events(self, raw_events: List[Dict], nbc_api: NBC = None):
        """Adds multiple raw clickstream events.

        Args:
            raw_events: List of raw clickstream events.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        ee = event.event.Events()
        ee.add_raw_events(raw_events)
        self.add_events(ee, nbc_api)

    def statistics_to_dict(self) -> dict:
        """Gets dictionary of fields in `statistics`. All nested dataclasses should be converted to dictionaries as
        well.

        Return:
            Dictionary representation of `statistics` field.
        """
        return self.statistics.to_dict()

    def statistics_from_dict(self, d: dict):
        """Fills `statistics` field by providing a dictionary representation. All nested dataclasses should be filled
        accordingly.

        Args:
            d: Dictionary representation of `statistics` field.
        """
        self.statistics = from_dict(data_class=Statistics, data=d)

    def import_statistics(self, client: utils.firestore.client):
        """Imports `statistics` field from Firestore, overwriting the field.

        Args:
            client: Firestore client instance.
        """
        d = utils.read_statistics_from_firestore(dmp_user_id=self.dmp_user_id, client=client)
        if d:
            self.statistics_from_dict(d)
        else:
            print(f'No `statistics` data found in the `{utils.USER_FIRESTORE_COLLECTION}` Firestore collection for '
                  f'`dmp_user_id`: `{self.dmp_user_id}`.')

    def export_statistics(self, client: utils.firestore.client):
        """Exports `statistics` field to Firestore, overwriting it.

        Args:
            client: Firestore client instance.
        """
        assert isinstance(self.statistics, Statistics), 'The `statistics` field needs to be a `Statistics` instance.'
        # assert self.statistics.validate(), \
        #     'User `statistics` are ill defined and could not be exported to Firestore. Tip: add at least one event ' \
        #     'to the user.'
        self.validate()
        self.statistics.validate()
        data = self.statistics.to_dict()
        utils.write_statistics_to_firestore(client=client, dmp_user_id=self.dmp_user_id, statistics=data)

    def create_user_from_clickstream(self, client: utils.firestore.client):
        """Gets all raw clickstream data and updates the user `statistics`.

        Args:
            client: Firestore client instance.
        """
        self.statistics = Statistics()  # Reset to default.
        data = utils.import_website_clickstream_events(client=client, dmp_user_id=self.dmp_user_id)
        self.add_raw_events(data)

    def update_user_from_clickstream(self, client: utils.firestore.client):
        """Gets all raw clickstream data that has occurred after the latest event tracked in the `statistics` and
        updates the user `statistics` with that data.

        Args:
            client: Firestore client instance.
        """
        data = utils.import_website_clickstream_events(
            client=client,
            dmp_user_id=self.dmp_user_id,
            timestamp_left_bound=self.statistics.general.activity_last_timestamp  # Okay if None, then all data is used.
        )
        self.add_raw_events(data)

    def validate(self):
        """Validate if fields are as desired."""
        # Force correct field types.
        for attr_name, attr_type in self.__annotations__.items():
            if not isinstance(getattr(self, attr_name), attr_type):
                raise ValueError(f'The value given in field `{attr_name}` is of a wrong type.')

        # print(getattr(self.statistics, 'validate')())
