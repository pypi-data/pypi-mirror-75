"""Pageview events.

Created: 2020-07-01 (Merijn, DAT-1583)
Updated: 2020-07-11 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
import re


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from .event import Event
from vaknl_user.event.utils import safe_list_get


# ----------------------------------------------------------------------------------------------------------------------
# Pageview dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Pageview(Event):
    """Pageview superclass.
    event_value_type == 'pageview'"""
    # url: str
    # page_type: str
    # The following (hidden) dummy is necessary to not create inheritance attribute order problems on defaults later on.
    dummy: int = field(repr=False, default=None)


# ----------------------------------------------------------------------------------------------------------------------
# Pageview sub-dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class PageviewHome(Pageview):
    """pageview_page_type == 'homePage'"""
    funnel_event: bool = False


@dataclass
class PageviewSearch(Pageview):
    """pageview_page_type in ('brandedSearchPage', 'Search', 'nonBrandedSearchPage', 'Branded Search')
    Last 2 are old ones from before 2019."""
    funnel_event: bool = False


@dataclass
class PageviewProduct(Pageview):
    """pageview_page_type == 'productPage'"""
    giata_id: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        self.giata_id = safe_list_get(re.findall(r"hotelId=(\d+)", event_value['pageview'].get('url')), 0, None)

    def _force_fields_not_none(self):
        fields = ['giata_id']
        self._raise_error_if_fields_are_none(fields)


@dataclass
class PageviewBookingStep(Pageview):
    """pageview_page_type == 'bookingForm'"""
    funnel_event: bool = False


@dataclass
class PageviewDeal(Pageview):
    """pageview_page_type == 'dealPage'"""
    funnel_event: bool = False


@dataclass
class PageviewKeuzehulp(Pageview):
    """pageview_page_type == 'searchAssistantPage'"""
    # page_type2: str
    funnel_event: bool = False


@dataclass
class PageviewContent(Pageview):
    """pageview_page_type == 'content'"""
    funnel_event: bool = False


@dataclass
class PageviewBlog(Pageview):
    """pageview_page_type == 'newsPage'"""
    funnel_event: bool = False


@dataclass
class PageviewError(Pageview):
    """pageview_page_type in ('errorPage', '404Page')"""
    funnel_event: bool = False


@dataclass
class PageviewOther(Pageview):
    """All other pageview events that are not defined as separate dataclass."""
    funnel_event: bool = False
