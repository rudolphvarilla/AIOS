"""
AIOS Background Scheduler
core/scheduler/manager.py

Coordinates the background queue.

Version 1:
Queue management only.
"""

from core.scheduler.queue import BackgroundQueue
from core.scheduler.worker import BackgroundWorker

class Scheduler:

    def __init__(self, time):

        self.time = time

        self.queue = BackgroundQueue(time)

        self.worker = BackgroundWorker(
            self.queue,
            time
        )