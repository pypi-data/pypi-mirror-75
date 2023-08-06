"""Reservation events.

Created: 2020-07-01 (Merijn, DAT-1583)
Updated: 2020-07-11 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from .event import Event


# ----------------------------------------------------------------------------------------------------------------------
# Reservation dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Reservation(Event):
    """Reservation superclass"""
    giata_id: str = None


# ----------------------------------------------------------------------------------------------------------------------
# Reservation sub-dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class ReservationExtras(Reservation):
    """event_trigger == 'ibe-extras'"""
    funnel_event: bool = False


@dataclass
class ReservationPersonalData(Reservation):
    """event_trigger == 'ibe-personaldata'"""
    funnel_event: bool = True


@dataclass
class ReservationOverview(Reservation):
    """event_trigger == 'ibe-overview-payment'"""
    funnel_event: bool = True


@dataclass
class ReservationBooked(Reservation):
    """event_trigger == 'ibe-confirmation' and reservation_status == 'Booked'"""
    reservation_id: str = None
    funnel_event: bool = True

    def _fill_event_from_event_value(self, event_value: dict):
        self.reservation_id = event_value.get('reservation', {}).get('reservationId')


@dataclass
class ReservationOther(Reservation):
    """All other reservation events that are not defined as separate dataclass."""
    reservation_status: str = None
    funnel_event: bool = False
