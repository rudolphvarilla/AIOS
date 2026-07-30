"""
===========================================================
AIOS Time Manager
core/time/manager.py
===========================================================

Single source of truth for time inside AIOS.

The Time Manager exposes every time-related function
used throughout AIOS while delegating all implementation
to the Time Service.

No subsystem should directly import datetime.

Future

• Timezone conversion
• Travel time calculations
• User time preferences
• Scheduler synchronization
• NTP synchronization
• World clock
===========================================================
"""

from core.time.service import TimeService


class TimeManager:

    def __init__(self):

        self.service = TimeService()

    # --------------------------------------------------
    # Current Date & Time
    # --------------------------------------------------

    def now(self):

        return self.service.now()

    def utc(self):

        return self.service.utc()

    def today(self):

        return self.service.today()

    def timestamp(self):

        return self.service.timestamp()

    # --------------------------------------------------
    # Components
    # --------------------------------------------------

    def date(self):

        return self.service.date()

    def time(self):

        return self.service.time()

    def weekday(self):

        return self.service.weekday()

    def month(self):

        return self.service.month()

    def year(self):

        return self.service.year()

    def hour(self):

        return self.service.hour()

    def minute(self):

        return self.service.minute()

    def second(self):

        return self.service.second()

    # --------------------------------------------------
    # Timezone
    # --------------------------------------------------

    def timezone(self):

        return self.service.now().astimezone().tzinfo