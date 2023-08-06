"""Utility functions/classes for `vaknl_user/user`.

Created: 2020-07-10 (Merijn, DAT-1583)
Updated: 2020-07-29 (Merijn, create_firestore_client used library change)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from typing import List, Dict, Union
import google.auth
# import firebase_admin
# from firebase_admin import credentials, firestore
from google.cloud import firestore


# ----------------------------------------------------------------------------------------------------------------------
# Constant variables
# ----------------------------------------------------------------------------------------------------------------------
CLICKSTREAM_FIRESTORE_COLLECTION = u'in_website_clickstream'
USER_FIRESTORE_COLLECTION = u'dmp_user'


# ----------------------------------------------------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------------------------------------------------
def create_firestore_client(project_id: str = None):
    """Sets up Firestore client.

    Args:
        project_id: GCP 'project id'.
    """
    if not project_id:
        _, project_id = google.auth.default()
    # cred = credentials.ApplicationDefault()
    # firebase_admin.initialize_app(cred, {'projectId': project_id})
    # return firestore.client()
    return firestore.Client(project=project_id)


def import_website_clickstream_events(client: firestore.Client, dmp_user_id: str, timestamp_left_bound: int = None) \
        -> List[Dict]:
    """Import raw website clickstream events from Firestore.

    Args:
        client: A Firestore client object.
        dmp_user_id: The `dmp_user_id` of the user.
        timestamp_left_bound: Unix timestamp for which all events need to have a greater timestamp to be included. If
            left `None`, all clickstream event data is used.

    Return:
        A list of raw website clickstream events.
    """
    # Get `dmp_session_id`s stored in Firestore for given `dmp_user_id`.
    doc_ref = client.collection(CLICKSTREAM_FIRESTORE_COLLECTION).document(dmp_user_id) \
        .collection(u'sessions').stream()
    sessions = [doc.id for doc in doc_ref]

    # Get all events.
    event_list = []
    for session in sessions:
        event_list += client.collection(CLICKSTREAM_FIRESTORE_COLLECTION).document(dmp_user_id) \
            .collection(u'sessions').document(session) \
            .collection(u'events').document(u'event_list').get().to_dict()['event_list']

    # Only take events greater than the `timestamp_left_bound`.
    if timestamp_left_bound is not None:
        event_list = [item for item in event_list if item.get('timestamp', 0) > timestamp_left_bound]

    return event_list


def read_statistics_from_firestore(client, dmp_user_id: str) -> Union[Dict, str]:
    """Import `statistics` of a user from Firestore.

    Args:
        client: A Firestore client object.
        dmp_user_id: The `dmp_user_id` of the user.

    Return:
        Dictionary with user statistics.
    """
    data = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id).get().to_dict()
    if data:
        data = data.get('statistics', None)
    return data


def write_statistics_to_firestore(client, dmp_user_id: str, statistics: Dict):
    """Write `statistics` of a user to the `dmp_user` collection in Firestore. Note: by using `set()` it overwrites the
    whole document.

    Args:
        client: A Firestore client object.
        dmp_user_id: The `dmp_user_id` of the user.
        statistics: The statistics dictionary that has to be written to Firestore.
    """
    doc_ref = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id)
    doc_ref.set({
        'statistics': statistics,
    })


def delete_dmp_user_firestore(client, dmp_user_id: str):
    """Deletes a Firestore document in the `dmp_user` collection with given `dmp_user_id`.

    Args:
        client: A Firestore client object.
        dmp_user_id: The `dmp_user_id` of the user.
    """
    doc_ref = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id)
    doc_ref.delete()
