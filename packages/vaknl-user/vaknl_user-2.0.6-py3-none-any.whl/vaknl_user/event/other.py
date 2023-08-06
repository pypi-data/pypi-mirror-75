"""All other events.

Created: 2020-07-01 (Merijn, DAT-1583)
Updated: 2020-07-11 (Merijn, DAT-1583)
"""

# TODO: add ppcVisitorAcco, which is a funnel event.


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import List


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from .event import Event


# ----------------------------------------------------------------------------------------------------------------------
# Other sub-dataclasses of Event
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Session(Event):
    """event_value_type == 'session'"""
    ip: str = None
    time_zone: str = None
    continent: str = None
    country: str = None
    region: str = None
    device: str = None
    funnel_event: bool = False

    def _fill_event_from_event_value(self, event_value: dict):
        self.device = event_value.get('session', {}).get('userAgent', {}).get('uaDeviceType')
        # Other attributes need to be set individually on creation, because the are not included in `event_value_json`.


@dataclass
class SearchPageSearchQuery(Event):
    """All filters applied in search on search page.
    event_value_type == 'search' and event_trigger == 'search'"""
    budget: int = None
    departure_airports: List[str] = field(default_factory=list)
    departure_date: str = None
    departure_date_flex: bool = None
    distance_to_beach: int = None
    durations: List[int] = field(default_factory=list)
    funnel_event: bool = True
    geo: List[str] = field(default_factory=list)
    meal_plans: List[str] = field(default_factory=list)
    min_hotel_rating: int = None
    min_star_rating: int = None
    party_composition: str = None
    theme: str = None

    def _fill_event_from_event_value(self, event_value: dict):
        filters = event_value.get('search', {}).get('filters')

        # Filter mapping from clickstream names to back-end names. Also includes default values that have to be
        # removed.
        filter_mapping = {
            'airports': {'name': 'departure_airports', 'remove_if': None},
            'budget': {'name': 'budget', 'remove_if': ['0']},
            'distanceToBeach': {'name': 'distance_to_beach', 'remove_if': ['0']},
            'departure': {'name': 'departure_date', 'remove_if': None},
            'duration': {'name': 'durations', 'remove_if': None},
            'geo': {'name': 'geo', 'remove_if': None},
            'hotelRatings': {'name': 'min_hotel_rating', 'remove_if': ['-1']},
            'mealplans': {'name': 'meal_plans', 'remove_if': None},
            'partyComposition': {'name': 'party_composition', 'remove_if': None},
            'rating': {'name': 'min_star_rating', 'remove_if': ['0']},
            'theme': {'name': 'theme', 'remove_if': ['geen_voorkeur']},
        }

        # Loop through filters of query.
        for fltr in filters:
            filter_name = fltr.get('filterName')
            if filter_name in filter_mapping.keys():
                remove_if = filter_mapping[filter_name]['remove_if']
                key = filter_mapping[filter_name]['name']

                # Get filter values.
                if filter_name in ['mealplans', 'theme']:
                    # Additionally: transform to lowercase and replace spaces with underscores.
                    value = [item.lower().replace(' ', '_') for item in fltr['filterValues'].values()]
                else:
                    value = list(fltr['filterValues'].keys())

                # Filters specific alterations.
                if value is not None and remove_if is not None and filter_name != 'partyComposition':
                    value = value[0] if value != remove_if else None
                elif value is not None and filter_name == 'partyComposition':
                    value = value[0]
                elif filter_name == 'departure' and value:
                    value = value[0]
                    flex = len(value) > 10
                    setattr(self, 'departure_date_flex', flex)
                    value = value[:10]
                elif filter_name == 'duration' and value:
                    if len(value) > 1:
                        value = [int(item) for item in value if item.isdigit()]
                    elif len(value) == 1:
                        item = value[0]
                        if '-' in item:
                            bounds = item.split('-')
                            value = list(range(int(bounds[0]), int(bounds[1]) + 1))

                if filter_name == 'distanceToBeach' and value == 'on-beach':
                    value = 0

                # Pass the non empty filters through.
                if value is not None:
                    value_type = SearchPageSearchQuery.__annotations__[key]
                    if 'typing.' not in str(value_type):
                        value = value_type(value)
                    # Set attribute.
                    setattr(self, key, value)


@dataclass
class KeuzehulpShowTop10(Event):
    """event_value_type == 'basic' and event_trigger == 'showTop10'"""
    funnel_event: bool = True


@dataclass
class PriceClick(Event):
    """event_value_type == 'priceClick'"""
    giata_id: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        self.giata_id = event_value['packagePrice']['productCode']


@dataclass
class ImageClick(Event):
    """event_value_type == 'basic' and event_trigger == 'imgClick'"""
    giata_id: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        self.giata_id = event_value['value']


@dataclass
class ProductService(Event):
    """event_type == 'productService'
    Is always: event_trigger in ('roomTypeSelection', 'mealPlanSelection', 'flightSelection')"""
    giata_id: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        self.giata_id = event_value.get('package', {}).get('productCode')


@dataclass
class ProductAvailability(Event):
    """event_type == 'productAvailability'
    Is always: event_trigger == 'packageAvailability'"""
    # No giata_id available
    funnel_event: bool = True


@dataclass
class SelectExtrasBookingStep(Event):
    """event_type == 'basic' and event_trigger in ('changeTransfer', 'changeInsurance', 'changeLuggage')"""
    # No giata_id available
    type: str = None
    funnel_event: bool = True


@dataclass
class SfmcId(Event):
    """SalesForce marketing cloud identity.
    event_type == 'basic' and event_trigger == 'sfmcId'"""
    email: str = None
    funnel_event: bool = False

    def _fill_event_from_event_value(self, event_value: dict):
        self.email = event_value.get('value', {}).get('email')


@dataclass
class EventOther(Event):
    """All other events that are not defined by the stated."""
    event_value_type: str = None
    event_trigger: str = None
    funnel_event: bool = False

    def _force_fields_not_none(self):
        fields = ['event_value_type', 'event_trigger']
        self._raise_error_if_fields_are_none(fields)
