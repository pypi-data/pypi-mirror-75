"""User statistics.

Contains dataclasses that keep track of several statistics when events are added.

Created: 2020-03-0? (Merijn)
Updated: 2020-07-30 (Merijn, DAT-1583)
"""

# TODO: improve section headers and structure.
# TODO: missing validate() methods in Statistic subclasses.


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Union
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_user import event
from vaknl_NBC import NBC


# ----------------------------------------------------------------------------------------------------------------------
# Statistic super dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Statistic:
    """Parent dataclass for all high level `XxxStatistics` dataclasses."""

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        # TODO: Make @abstractmethod.
        """Dummy function. Should be overwritten in child dataclass when used. Purpose: should update statistics by
        adding single event."""
        pass

    def validate(self):
        # TODO: Make @abstractmethod.
        """Dummy function. Should be overwritten in child dataclass when used. Purpose: validate if statistics are in
        correct format."""
        pass


# ----------------------------------------------------------------------------------------------------------------------
# Field label information dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class LabelInfo:
    """Keeps track of label statistics, by adding labels separately. Similar structure as `Statistic` only no nbc_api is
     included."""
    count: int = 0
    frequency: Dict[Any, int] = field(default_factory=dict)
    last: Union[str, int, None] = None

    def add_label(self, label: Union[str, int]):
        """Adds single label."""
        self.last = label
        if label is not None:
            label = str(label)
            self.count += 1
            self.frequency[label] = self.frequency[label] + 1 if label in self.frequency else 1


@dataclass
class LabelListInfo:
    """Keeps track of label statistics, by adding lists of labels (multi-label). Similar structure as `Statistic` only
    no nbc_api is included."""
    frequency: Dict[Any, int] = field(default_factory=dict)

    def add_labels(self, labels: List[Union[str, int]]):
        """Adds list of labels."""
        for label in labels:
            label = str(label)
            self.frequency[label] = self.frequency[label] + 1 if label in self.frequency else 1


# ----------------------------------------------------------------------------------------------------------------------
# Specific `Statistic` sub-sub dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class SearchPageSearchQueryStatistics(Statistic):
    """Statistics on the search query event on search page (`event.other.SearchPageSearchQuery`)."""
    budget: LabelInfo = field(default_factory=LabelInfo)
    count: int = 0
    departure_airports: LabelListInfo = field(default_factory=LabelListInfo)
    departure_date: LabelInfo = field(default_factory=LabelInfo)
    departure_date_flex: LabelInfo = field(default_factory=LabelInfo)
    distance_to_beach: LabelInfo = field(default_factory=LabelInfo)
    durations: LabelListInfo = field(default_factory=LabelListInfo)
    geo: LabelListInfo = field(default_factory=LabelListInfo)
    meal_plans: LabelListInfo = field(default_factory=LabelListInfo)
    min_hotel_rating: LabelInfo = field(default_factory=LabelInfo)
    min_star_rating: LabelInfo = field(default_factory=LabelInfo)
    party_composition: LabelInfo = field(default_factory=LabelInfo)
    theme: LabelInfo = field(default_factory=LabelInfo)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        if isinstance(evt, event.other.SearchPageSearchQuery):
            self.count += 1

            # Fields with LabelInfo.
            self.budget.add_label(evt.budget)
            self.departure_date.add_label(evt.departure_date)
            self.departure_date_flex.add_label(evt.departure_date_flex)
            self.distance_to_beach.add_label(evt.distance_to_beach)
            self.min_hotel_rating.add_label(evt.min_hotel_rating)
            self.min_star_rating.add_label(evt.min_star_rating)
            self.party_composition.add_label(evt.party_composition)
            self.theme.add_label(evt.theme)

            # Fields with LabelListInfo
            self.departure_airports.add_labels(evt.departure_airports)
            self.durations.add_labels(evt.durations)
            self.geo.add_labels(evt.geo)
            self.meal_plans.add_labels(evt.meal_plans)


# ----------------------------------------------------------------------------------------------------------------------
# Statistics sub dataclasses used in Statistics
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class GeneralStatistics(Statistic):
    """General statistics of a user."""
    activity_first_timestamp: int = None
    activity_last_timestamp: int = None
    event_cnt: int = field(default=0)
    funnel_step: str = None  # = 'visitor'; the funnel names could change
    pageview_cnt: int = field(default=0)
    user_identifiers: Dict[str, List] = field(default_factory=dict)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        t = evt.timestamp
        self.activity_first_timestamp = min(elem for elem in [self.activity_first_timestamp, t] if elem is not None)
        self.activity_last_timestamp = max(elem for elem in [self.activity_last_timestamp, t] if elem is not None)
        self.event_cnt += 1 if isinstance(evt, event.event.Event) else 0
        self.pageview_cnt += 1 if isinstance(evt, event.pageview.Pageview) else 0
        if isinstance(evt, event.other.SfmcId):
            if evt.email and evt.email != 'undefined':
                self.user_identifiers['email'] = list(set(self.user_identifiers.get('email', []) + [evt.email]))


@dataclass
class OtherStatistics(Statistic):
    """Statistics of a user that don't belong to one of the other categories."""
    filter_party_composition_freq: Dict = field(default_factory=dict)
    keuzehulp_show_top10_cnt: int = field(default=0)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        if isinstance(evt, event.filter.GlobalFilterPartyComposition):
            self.filter_party_composition_freq[evt.label] = self.filter_party_composition_freq[evt.label] + 1 \
                if evt.label in self.filter_party_composition_freq else 1
        self.keuzehulp_show_top10_cnt += 1 if isinstance(evt, event.other.KeuzehulpShowTop10) else 0


@dataclass
class ProductStatistics(Statistic):
    """Statistics of the behaviour of a user on the product pages."""
    availability_check_cnt: int = field(default=0)
    filter_airport_cnt: int = field(default=0)
    filter_departure_date_cnt: int = field(default=0)
    filter_meal_plan_cnt: int = field(default=0)
    filter_flight_cnt: int = field(default=0)
    image_click_cnt: int = field(default=0)
    giata_id: LabelInfo = field(default_factory=LabelInfo)
    price_click_cnt: int = field(default=0)
    service_cnt: int = field(default=0)

    # NBC:
    country_code: LabelInfo = field(default_factory=LabelInfo)
    region_id: LabelInfo = field(default_factory=LabelInfo)
    city_id: LabelInfo = field(default_factory=LabelInfo)
    theme: LabelListInfo = field(default_factory=LabelListInfo)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        self.availability_check_cnt += 1 if isinstance(evt, event.other.ProductAvailability) else 0
        self.filter_airport_cnt += 1 if isinstance(evt, event.filter.ProductPageFilterAirport) else 0
        self.filter_departure_date_cnt += 1 if isinstance(evt, event.filter.ProductPageFilterDepDate) else 0
        self.filter_meal_plan_cnt += 1 if isinstance(evt, event.filter.ProductPageFilterMealPlan) else 0
        self.filter_flight_cnt += 1 if isinstance(evt, event.filter.ProductPageFilterFlight) else 0
        self.image_click_cnt += 1 if isinstance(evt, event.other.ImageClick) else 0
        self.price_click_cnt += 1 if isinstance(evt, event.other.PriceClick) else 0
        self.service_cnt += 1 if isinstance(evt, event.other.ProductService) else 0
        if isinstance(evt, event.pageview.PageviewProduct):
            self.giata_id.add_label(evt.giata_id)
            data = nbc_api.get_by_giata_id(int(evt.giata_id))
            if data:
                self.country_code.add_label(data.get('country_code'))
                self.region_id.add_label(data.get('region_id'))
                self.city_id.add_label(data.get('city_id'))
                themes = [
                    key for key, value in data.items() if ('theme_' in key) and (key != 'theme_main') and int(value)
                ]
                self.theme.add_labels(themes)


@dataclass
class ReservationStatistics(Statistic):
    """Statistics of the behaviour of a user in the booking steps."""
    booking: LabelInfo = field(default_factory=LabelInfo)
    extras_cnt: int = field(default=0)
    extras_select_extras_cnt: int = field(default=0)
    overview_cnt: int = field(default=0)
    pageview_cnt: int = field(default=0)
    personal_data_cnt: int = field(default=0)
    reservation_id_freq: List[str] = field(default_factory=list)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        if isinstance(evt, event.reservation.ReservationBooked):
            if evt.reservation_id not in self.reservation_id_freq and evt.reservation_id is not None:
                self.reservation_id_freq.append(evt.reservation_id)
                self.booking.add_label(evt.giata_id)
        self.extras_cnt += 1 if isinstance(evt, event.reservation.ReservationExtras) else 0
        self.extras_select_extras_cnt += 1 if isinstance(evt, event.other.SelectExtrasBookingStep) else 0
        self.overview_cnt += 1 if isinstance(evt, event.reservation.ReservationOverview) else 0
        self.pageview_cnt += 1 if isinstance(evt, event.pageview.PageviewBookingStep) else 0
        self.personal_data_cnt += 1 if isinstance(evt, event.reservation.ReservationPersonalData) else 0


@dataclass
class SearchStatistics(Statistic):
    """Statistics of the behaviour of a user on the search page."""
    filter_select_cnt: int = field(default=0)
    pageview_cnt: int = field(default=0)
    search_query: SearchPageSearchQueryStatistics = field(default_factory=SearchPageSearchQueryStatistics)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        self.filter_select_cnt += 1 if isinstance(evt, event.filter.SearchPageFilter) else 0
        self.pageview_cnt += 1 if isinstance(evt, event.pageview.PageviewSearch) else 0
        self.search_query.add_event(evt, nbc_api)


@dataclass
class SessionStatistics(Statistic):
    """Statistics on sessions of a user."""
    count: int = field(default=0)
    day_of_week_freq: LabelInfo = field(default_factory=LabelInfo)
    dmp_session_id_list: List[str] = field(default_factory=list)
    hour_of_day_freq: LabelInfo = field(default_factory=LabelInfo)

    def add_event(self, evt: event.event.Event, nbc_api: NBC):
        """Method information in parent dataclass."""
        self.dmp_session_id_list = list(set(self.dmp_session_id_list + [evt.dmp_session_id]))
        self.count = len(self.dmp_session_id_list)
        if isinstance(evt, event.other.Session):
            date_time = datetime.fromtimestamp(evt.timestamp / 1e3)
            self.day_of_week_freq.add_label(date_time.weekday())  # Day of week as number: 0-6 (Monday-Sunday)
            self.hour_of_day_freq.add_label(date_time.hour)


# ----------------------------------------------------------------------------------------------------------------------
# Statistics dataclass used in User
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Statistics:
    """A collection of several different categories of statistics. Highest statistics field in the hierarchy."""
    general: GeneralStatistics = field(default_factory=GeneralStatistics)
    other: OtherStatistics = field(default_factory=OtherStatistics)
    product: ProductStatistics = field(default_factory=ProductStatistics)
    reservation: ReservationStatistics = field(default_factory=ReservationStatistics)
    search: SearchStatistics = field(default_factory=SearchStatistics)
    session: SessionStatistics = field(default_factory=SessionStatistics)

    def __post_init__(self):
        # Force correct field types.
        self.validate()

    def add_event(self, evt: event.event.Event, nbc_api: NBC = None, update_funnel_step: bool = True):
        """Adds single event to update statistics.

        Args:
            evt: An event.
            nbc_api: NBC API instance.
            update_funnel_step: Indicator for updating the `funnel_step` in statistics. For batches of events, it is not
                necessary to update the funnel step per every added event.
        """
        if nbc_api is None:
            nbc_api = NBC()
        self.general.add_event(evt, nbc_api)
        self.other.add_event(evt, nbc_api)
        self.product.add_event(evt, nbc_api)
        self.reservation.add_event(evt, nbc_api)
        self.search.add_event(evt, nbc_api)
        self.session.add_event(evt, nbc_api)
        if update_funnel_step:
            self.update_funnel_step()

    def add_events(self, evts: event.event.Events, nbc_api: NBC = None):
        """Adds multiple events to update statistics.

        Args:
            evts: An Events instance.
            nbc_api: NBC API instance.
        """
        evts.sort_by_timestamp_ascending()
        if nbc_api is None:
            nbc_api = NBC()
        for item in evts.event_list:
            self.add_event(item, nbc_api, update_funnel_step=False)
        self.update_funnel_step()

    def validate(self):
        """Validate if fields are as desired."""
        for attr_name, attr_type in self.__annotations__.items():
            if not isinstance(getattr(self, attr_name), attr_type):
                raise ValueError(f'The value given in field `{attr_name}` is of a wrong type.')

    def to_dict(self):
        """Get dictionary of fields. All nested dataclasses should be converted to dictionaries as well."""
        self.validate()
        return asdict(self)

    def update_funnel_step(self):
        """Update the funnel step in accordance on the basis of the current statistic fields."""
        # TODO: add ppcVisitorAcco, which is a funnel event.
        # TODO: Simplify funnel to eliminate 'other' events.
        current_step = self.general.funnel_step
        if current_step != 'booked':
            # Check if funnel step can be updated to 'booked'.
            if self.reservation.booking.count > 0:
                self.general.funnel_step = 'booked'
            elif current_step != 'in_market':
                # Check if funnel step can be updated to 'in_market'.
                if (
                        self.reservation.personal_data_cnt + self.reservation.overview_cnt
                        + self.reservation.extras_select_extras_cnt
                ) > 0:
                    self.general.funnel_step = 'in_market'
                elif current_step != 'active_plus':
                    # Check if funnel step can be updated to 'active_plus'.
                    if self.product.availability_check_cnt or self.product.filter_airport_cnt or \
                            self.product.filter_flight_cnt or self.product.filter_meal_plan_cnt or \
                            self.product.service_cnt or self.reservation.extras_cnt or \
                            self.product.image_click_cnt >= 5:
                        self.general.funnel_step = 'active_plus'
                    elif current_step != 'active':
                        # Check if funnel step can be updated to 'active'.
                        if self.search.search_query.departure_date.count or self.product.filter_departure_date_cnt or \
                                bool(self.other.filter_party_composition_freq) or \
                                self.other.keuzehulp_show_top10_cnt or self.product.image_click_cnt >= 3 or \
                                self.search.filter_select_cnt >= 2:
                            self.general.funnel_step = 'active'
                        else:
                            # If it doe not belong to any other funnel steps, the default is 'visitor'.
                            self.general.funnel_step = 'visitor'
