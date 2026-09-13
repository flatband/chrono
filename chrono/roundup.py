# roundup.py
"""Round a datetime or time up to the next multiple of a unit."""

import datetime as _dt
from typing import Literal

_UNITS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
}
_DAY = _dt.timedelta(days=1)


def roundup(value, amount: float, unit: Literal["s", "m", "h"]):
    """Return `value` rounded up to the next multiple of `amount` `unit`.

    value  -- a datetime (aware or naive) or a time.
    amount -- positive step size.
    unit   -- one of "s", "m", "h".

    Steps count from the value's midnight in wall-clock time, so 15 "m"
    lands on :00/:15/:30/:45. A grid that doesn't divide the day evenly
    stops at the next midnight, so 24 "h" rounds up to the next midnight.
    A value already on the grid is returned unchanged.

    A time raises OverflowError if the result would be 24:00 or later.
    """
    if unit not in _UNITS:
        raise ValueError(f"Unknown unit {unit!r}: expected one of {sorted(_UNITS)}.")
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount!r}.")
    step = _dt.timedelta(**{_UNITS[unit]: amount})

    if isinstance(value, _dt.datetime):
        midnight = value.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight + _ceil(value - midnight, step)

    if isinstance(value, _dt.time):
        since_midnight = _dt.timedelta(
            hours=value.hour,
            minutes=value.minute,
            seconds=value.second,
            microseconds=value.microsecond,
        )
        rounded = _ceil(since_midnight, step)
        if rounded >= _DAY:
            raise OverflowError(f"Rounding {value!r} up by {amount} {unit!r} passes midnight.")
        return (_dt.datetime.min + rounded).time().replace(tzinfo=value.tzinfo)

    raise TypeError(f"Can't round {value!r}: expected a datetime or time.")


def _ceil(elapsed, step):
    return min(-(-elapsed // step) * step, _DAY)
