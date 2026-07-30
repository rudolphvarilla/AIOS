"""
AIOS Provider Manager Tests
"""

from core.providers.manager import ProviderManager


manager = ProviderManager()


print("=" * 40)
print("AVAILABLE PROVIDERS")
print("=" * 40)

for provider in manager.list_providers():

    print(provider)

print()

print("=" * 40)
print("EXISTS TEST")
print("=" * 40)

print(manager.exists("DUCKDUCKGO"))
print(manager.exists("TEST"))

print()

print("=" * 40)
print("GET TEST")
print("=" * 40)

print(manager.get("DUCKDUCKGO"))

print()

print("=" * 40)
print("SELECT TEST")
print("=" * 40)

print()

print(manager.select("SEARCH"))