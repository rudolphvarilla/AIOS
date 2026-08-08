"""
AIOS Provider Manager
core/providers/manager.py

Selects providers for requested services.

Supports

Priority ordering
Automatic failover
Multi-provider selection

Version 2
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
    # Candidate selection
    # --------------------

    def select_all(self, service):
        """Return all available providers for a service in priority order."""

        candidates = [
            provider
            for provider in self.providers.values()
            if provider.service == service
            and provider.available
            and provider.instance is not None
        ]

        candidates.sort(key=lambda p: p.priority)

        return [provider.instance for provider in candidates]

    # --------------------
    # Select one
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
                and provider.instance is not None
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
