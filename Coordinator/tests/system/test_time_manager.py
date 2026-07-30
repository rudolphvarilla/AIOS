from core.time.service import TimeService

time = TimeService()

print(time.now())
print(time.utc())
print(time.today())
print(time.timestamp())