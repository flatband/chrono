# waiter.py
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Literal

from .time_parser import to_datetime

logger = logging.getLogger(__name__)

_UNITS = {
    "s": (1, "seconds"),
    "m": (60, "minutes"),
    "h": (3600, "hours"),
    "d": (86400, "days"),
}


async def wait_until(date=None, time=None, timezone=None):
    """Sleep until the given date and time.

    Arguments match `to_datetime`. If `date` is omitted, only a time of
    day is targeted: a time already past today rolls over to tomorrow.
    If `date` is given explicitly and the resulting datetime is already
    past, returns immediately without waiting.
    """
    target = to_datetime(date=date, time=time, timezone=timezone)

    delay = (target - datetime.now(target.tzinfo)).total_seconds()
    if delay <= 0:
        if date is None:
            target = target + timedelta(days=1)
            delay = (target - datetime.now(target.tzinfo)).total_seconds()
        else:
            logger.info(f"{target} is in the past; not waiting.")
            return

    logger.info(f"Waiting until {target} ({delay:.1f}s).")
    await asyncio.sleep(delay)


async def wait_for(duration: float, units: Literal["s", "m", "h", "d"] = "s"):
    """Sleep for `duration` in the given units."""
    if units not in _UNITS:
        raise ValueError(f"Unknown unit {units!r}: expected one of {sorted(_UNITS)}.")

    factor, name = _UNITS[units]
    logger.debug(f"Waiting for {duration:.2f} {name}.")
    await asyncio.sleep(duration * factor)