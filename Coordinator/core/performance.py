import time


class PerformanceMonitor:

    def __init__(self):

        self.times = {}

    def start(self, stage):

        self.times[stage] = {
            "start": time.perf_counter()
        }

    def stop(self, stage):

        self.times[stage]["end"] = time.perf_counter()

        self.times[stage]["elapsed"] = (
            self.times[stage]["end"]
            - self.times[stage]["start"]
        )

    def report(self):

        print("\n----- PERFORMANCE -----")

        total = 0.0

        for stage, data in self.times.items():

            elapsed = data["elapsed"]

            total += elapsed

            print(f"{stage:<25} {elapsed:.4f} s")

        print("-" * 38)
        print(f"{'TOTAL':<25} {total:.4f} s")