"""
AIOS Provider Manager
core/providers/manager.py

Selects the best provider
for a requested service.

Supports

Priority ordering

Automatic failover

Version 1
"""

from core.providers.registry import PROVIDERS


class ProviderManager:

    def __init__(self):

        self.providers = PROVIDERS

    # --------------------
    # Register Provider
    # --------------------

    def register(self, name, config):

        self.providers[name] = config

    # --------------------
    # Exists
    # --------------------

    def exists(self, name):

        return name in self.providers

    # --------------------
    # Get
    # --------------------

    def get(self, name):

        return self.providers.get(name)

    # --------------------
    # List
    # --------------------

    def list_providers(self):

        return list(self.providers.keys())

    # --------------------
    # Select
    # --------------------

    def select(self, service):

        print("\nSelecting provider...")
        print(f"Requested Service : {service}")

        candidates = [

            provider

            for provider in self.providers.values()

            if (
                provider.service == service
                and provider.available
            )

        ]

        candidates.sort(
            key=lambda p: p.priority
        )

        if len(candidates) == 0:

            print("No provider available.")

            return None

        selected = candidates[0]

        print(f"Selected -> {selected.name}")

        return selected.instance