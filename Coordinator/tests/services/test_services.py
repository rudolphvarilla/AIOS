"""
AIOS Service Manager Tests
"""

from core.services.manager import ServiceManager


manager = ServiceManager()

print("=" * 40)
print("AVAILABLE SERVICES")
print("=" * 40)

for service in manager.list_services():

    print(service)

print()

print("=" * 40)
print("SELECT SERVICE")
print("=" * 40)

service = manager.select("SEARCH")

print(service)