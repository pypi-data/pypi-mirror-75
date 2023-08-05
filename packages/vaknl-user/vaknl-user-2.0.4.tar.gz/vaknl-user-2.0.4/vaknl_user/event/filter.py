"""Filter events.

Created: 2020-07-01 (Merijn, DAT-1583)
Updated: 2020-07-11 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from .event import Event


# ----------------------------------------------------------------------------------------------------------------------
# Filter dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Filter(Event):
    """Filter parent class"""
    # The following (hidden) dummy is necessary to avoid inheritance attribute order problems on defaults later on.
    dummy: int = field(repr=False, default=None)


# ----------------------------------------------------------------------------------------------------------------------
# Filter sub-dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class SearchPageFilter(Filter):
    """Any filter adjustment on search page, except for party composition and departure date
    event_value_type == 'basic' and event_trigger == 'selectFilter'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterDepDate(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterDepartureDate'"""


@dataclass
class ProductPageFilterAirport(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterAirport'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterMealPlan(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterMealplan'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterFlight(Filter):
    """Any of the flight filters.
    event_value_type == 'basic' and event_trigger == 'selectFlightFilter'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterDurationRange(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterDurationRange'"""
    funnel_event: bool = False


@dataclass
class GlobalFilterPartyComposition(Filter):
    """Event for party composition everywhere on the site.
    event_value_type == 'basic' and event_trigger == 'partyCompositionFilter'"""
    label: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        value = event_value.get('label', None)
        if isinstance(value, str):
            value = 'A' + value.replace('Adult', 'C').replace('Child', 'B').replace('Baby', '').replace(' ', '')
        self.label = value
