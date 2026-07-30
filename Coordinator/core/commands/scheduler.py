"""
AIOS Scheduler Commands

Commands related to the Background Scheduler.

Current Commands:
- /jobs
"""

def jobs_command(scheduler):

    print()

    print("=" * 60)
    print("BACKGROUND JOB QUEUE")
    print("=" * 60)

    print()

    print(f"Pending Jobs : {scheduler.queue.count()}")

    if scheduler.queue.count() ==0:

        print()

        print("No pending jobs.")

        return

    for i, job in enumerate(scheduler.queue.list_jobs(), start=1):

        print()

        print(f"[{i}]")

        print(f"Status      : {job.status}")

        print(f"Description : {job.description}")

        print(f"Created     : {job.timestamp}")

def run_jobs_command(scheduler):

    print()

    print("=" * 60)
    print("RUNNING BACKGROUND JOBS")
    print("=" * 60)

    print()

    completed = scheduler.worker.execute_all()

    print()

    print(f"Jobs Executed : {completed}")

def results_command(scheduler):

    print()

    print("=" * 60)
    print("BACKGROUND RESULTS")
    print("=" * 60)

    found = False

    for i, job in enumerate(scheduler.queue.jobs, start=1):

        if job.status == JOB_COMPLETE:

            found = True

            print()

            print(f"Job {i}")

            print(f"Description : {job.description}")

            print(f"Completed   : {job.completed_timestamp}")

            print()

            print("Result:")

            print(job.result)

            print("-" * 60)

    if not found:

        print()

        print("No completed jobs.")