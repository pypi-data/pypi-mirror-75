"""Event module.

Imports all child modules and includes a `create_event()` function.

Created: 2020-07-01 (Merijn, DAT-1583)
Updated: 2020-08-05 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union
import json
import re


# ----------------------------------------------------------------------------------------------------------------------
# Import child modules
# ----------------------------------------------------------------------------------------------------------------------
from . import event
from . import filter
from . import other
from . import pageview
from . import reservation


# ----------------------------------------------------------------------------------------------------------------------
# Create event function
# ----------------------------------------------------------------------------------------------------------------------
def create_event(data: dict) -> Union[event.Event, None]:
    """Assigns event to an event-dataclass based on the event clickstream data and sends additional event-specific
    kwargs to event object on creation.

    Args:
        data: Dictionary describing a clickstream event.

    Return:
        Event dataclass object.
    """
    if not isinstance(data, dict):
        raise TypeError('The field `data` should be of type `dict`.')
    event_value_type = data['eventValueType']
    if event_value_type == 'undefined':
        return None
    else:
        event_trigger = data['info']['eventTrigger']
        kwargs = dict(
            event_id=data['eventId'],
            timestamp=data['timestamp'],
            dmp_session_id=data['info']['dmpSessionId'],
            event_value=json.loads(data['eventValueJson']),

        )
        event_value_type_mapper = {
            'session': other.Session,
            'priceClick': other.PriceClick,
            'productAvailability': other.ProductAvailability,
            'productService': other.ProductService,
        }
        if event_value_type in event_value_type_mapper.keys():
            event_class = event_value_type_mapper[event_value_type]
            if event_value_type == 'session':
                kwargs.update(dict(
                    ip=data.get('remoteIp'),
                    time_zone=data.get('timeZone'),
                    continent=data.get('continent'),
                    country=data.get('country'),
                    region=data.get('mostSpecificSubdivision'),
                ))
        elif event_value_type == 'pageview':
            page_type_mapper = {
                'homePage': pageview.PageviewHome,
                'productPage': pageview.PageviewProduct,
                'brandedSearchPage': pageview.PageviewSearch,
                'Search': pageview.PageviewSearch,
                'nonBrandedSearchPage': pageview.PageviewSearch,
                'Branded Search': pageview.PageviewSearch,
                'bookingForm': pageview.PageviewBookingStep,
                'dealPage': pageview.PageviewDeal,
                'searchAssistantPage': pageview.PageviewKeuzehulp,
                'content': pageview.PageviewContent,
                'newsPage': pageview.PageviewBlog,
                'errorPage': pageview.PageviewError,
                '404Page': pageview.PageviewError,
            }
            page_type = kwargs['event_value'].get(event_value_type, {}).get('pageType')
            event_class = page_type_mapper.get(page_type, pageview.PageviewOther)
        elif event_value_type == 'reservation':
            reservation_status = kwargs['event_value'].get(event_value_type, {}).get('reservationStatus')
            kwargs['giata_id'] = kwargs['event_value']['reservation']['packages'][0]['productCode']
            if event_trigger == 'ibe-extras':
                event_class = reservation.ReservationExtras
            elif event_trigger == 'ibe-personaldata':
                event_class = reservation.ReservationPersonalData
            elif event_trigger == 'ibe-overview-payment':
                event_class = reservation.ReservationOverview
            elif event_trigger == 'ibe-confirmation' and reservation_status == 'Booked':
                event_class = reservation.ReservationBooked
            else:
                kwargs.update(dict(reservation_status=reservation_status))
                event_class = reservation.ReservationOther
        elif event_value_type == 'search' and event_trigger == 'search':
            event_class = other.SearchPageSearchQuery
        elif event_value_type == 'basic':
            event_trigger_mapper = {
                'imgClick': other.ImageClick,
                'selectFilter': filter.SearchPageFilter,
                'filterDepartureDate': filter.ProductPageFilterDepDate,
                'filterAirport': filter.ProductPageFilterAirport,
                'filterMealplan': filter.ProductPageFilterMealPlan,
                'selectFlightFilter': filter.ProductPageFilterFlight,
                'filterDurationRange': filter.ProductPageFilterDurationRange,
                'partyCompositionFilter': filter.GlobalFilterPartyComposition,
                'changeTransfer': other.SelectExtrasBookingStep,
                'changeInsurance': other.SelectExtrasBookingStep,
                'changeLuggage': other.SelectExtrasBookingStep,
                'showTop10': other.KeuzehulpShowTop10,
                'sfmcId': other.SfmcId,
            }
            if event_trigger in event_trigger_mapper.keys():
                event_class = event_trigger_mapper[event_trigger]
            else:
                kwargs.update(dict(
                    event_value_type=event_value_type,
                    event_trigger=event_trigger,
                ))
                event_class = other.EventOther

            if event_class == other.SelectExtrasBookingStep:
                kwargs.update(dict(type=re.findall(r"change(.+)", event_trigger.lower())[0]))
        else:
            kwargs.update(dict(
                event_value_type=event_value_type,
                event_trigger=event_trigger,
            ))
            event_class = other.EventOther

        return event_class(**kwargs)
