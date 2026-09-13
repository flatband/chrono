import datetime
def is_past(value: datetime) -> bool:
    """Return whether `value` is before the current time.

    Naive datetimes are compared against the local system time; aware
    datetimes are compared in their own timezone.
    """
    now = datetime.now(value.tzinfo)
    return value < now