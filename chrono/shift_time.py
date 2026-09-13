# time_calculator.py
"""Shift a datetime by a signed amount of time."""

import datetime as _dt
from typing import Literal

_DURATION_UNITS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
}
_UNITS = {**_DURATION_UNITS, "d": "days"}


def shift_time(value: _dt.datetime, amount: float, unit: Literal["s", "m", "h", "d"]):
    """Return `value` shifted by `amount` of `unit`.

    value  -- a datetime (aware or naive).
    amount -- signed number of units; negative moves earlier. Whole
              numbers only for unit "d".
    unit   -- one of "s", "m", "h" (real elapsed duration: exactly that
              many seconds later/earlier, computed through UTC so it's
              correct across a DST change), or "d" (calendar day: same
              wall-clock time on a date `amount` days away, matching
              `to_datetime`'s `day_offset`).

    Plain `aware_datetime + timedelta` silently does wall-clock
    arithmetic, not real-time arithmetic: it adds to the naive fields
    and lets the zone recompute the offset, so "+24h" and "+1 day" both
    land on the same clock time even when a DST change makes them 23 or
    25 real hours apart. "s"/"m"/"h" here route through UTC to avoid
    that; "d" is calendar arithmetic on purpose, so it keeps the
    wall-clock-preserving behavior.
    """
    if not isinstance(value, _dt.datetime):
        raise TypeError(f"Can't shift {value!r}: expected a datetime.")
    if unit not in _UNITS:
        raise ValueError(f"Unknown unit {unit!r}: expected one of {sorted(_UNITS)}.")

    if unit == "d":
        if amount != int(amount):
            raise ValueError(f"Whole days only for unit 'd', got {amount!r}.")
        return value + _dt.timedelta(days=int(amount))

    delta = _dt.timedelta(**{_DURATION_UNITS[unit]: amount})
    if value.tzinfo is None:
        return value + delta
    return (value.astimezone(_dt.timezone.utc) + delta).astimezone(value.tzinfo)
