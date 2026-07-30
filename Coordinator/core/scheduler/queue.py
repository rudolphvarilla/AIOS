"""
AIOS Background Queue
core/scheduler/queue.py

Stores pending background jobs.

Version 1:
- Queue only
- No execution

Job Status Values
Pending  : Waiting to be executed.
Running  : Currently being processed.
Complete : Finished successfully.
Failed   : Finished with an error.
"""

from dataclasses import dataclass

JOB_PENDING = "PENDING"
JOB_RUNNING = "RUNNING"
JOB_COMPLETE = "COMPLETE"
JOB_FAILED = "FAILED"

@dataclass
class BackgroundJob:

    timestamp: str

    description: str

    status: str

    result: str

    completed_timestamp: str

class BackgroundQueue:

    def __init__(self,time):

        self.time = time
        self.jobs = []

    #--------------------------
    #Add Job
    #--------------------------

    def add_job(self, description):

        job = BackgroundJob(
            timestamp=self.time.timestamp(),
            description=description,
            status=JOB_PENDING,
            result="",
            completed_timestamp=""
        )

        self.jobs.append(job)

    #--------------------------
    #Count Job
    #--------------------------

    def count(self):

        count = 0

        for job in self.jobs:

            if job.status == JOB_PENDING:

                count += 1

        return count

    #--------------------------
    #Clear Queue
    #--------------------------

    def clear(self):

        self.jobs.clear()

    #--------------------------
    #List Jobs
    #--------------------------

    def list_jobs(self):

        return self.jobs