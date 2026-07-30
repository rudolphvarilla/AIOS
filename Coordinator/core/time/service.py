"""
===========================================================
AIOS Time Service
core/time/service.py
===========================================================

Provides all date and time operations for AIOS.

Future versions may integrate:

• Timezone conversion
• Travel time calculations
• User locale preferences
• Scheduler synchronization
• NTP synchronization
• World clock support
===========================================================
"""

from datetime import datetime, timezone


class TimeService:

    def now(self):

        return datetime.now()

    def utc(self):

        return datetime.now(timezone.utc)

    def today(self):

        return self.now().date()

    def timestamp(self):

        return self.now().isoformat()

    def time(self):

        return self.now().time()

    def date(self):

        return self.now().date()

    def weekday(self):

        return self.now().strftime("%A")

    def month(self):

        return self.now().strftime("%B")

    def year(self):

        return self.now().year

    def hour(self):

        return self.now().hour

    def minute(self):

        return self.now().minute

    def second(self):

        return self.now().second