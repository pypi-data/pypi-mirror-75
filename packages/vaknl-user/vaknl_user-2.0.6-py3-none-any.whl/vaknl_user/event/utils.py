"""Utilities

Helper functions.

Created: 2020-07-10 (Merijn, DAT-1583)
Updated:
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# User defined functions
# ----------------------------------------------------------------------------------------------------------------------
def safe_list_get(lst: list, idx: int, default=None):
    """Safely get element with given index from list. A default value is returned when IndexError is raised or when the
    presented object is not a list.

    Args:
        lst: List object.
        idx: Index number of element in list.
        default: Default value to return in case of IndexError or when `lst` object is not a list.

    Return:
        Element from list or given `default` value.
    """
    if isinstance(lst, list):
        try:
            return lst[idx]
        except IndexError:
            return default
    else:
        return default
