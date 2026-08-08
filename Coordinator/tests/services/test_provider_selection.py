"""Tests for multi-provider selection."""

from dataclasses import replace

from core.providers.manager import ProviderManager
from core.providers.registry import PROVIDERS


def test_select_all_returns_available_search_providers_in_priority_order():
    manager = ProviderManager()
    original = dict(manager.providers)

    try:
        manager.providers = {
            "SECOND": replace(
                PROVIDERS["DUCKDUCKGO"],
                name="Second",
                priority=20,
            ),
            "FIRST": replace(
                PROVIDERS["DUCKDUCKGO"],
                name="First",
                priority=10,
            ),
        }

        providers = manager.select_all("SEARCH")

        assert len(providers) == 2
        assert providers[0] is manager.providers["FIRST"].instance
        assert providers[1] is manager.providers["SECOND"].instance
    finally:
        manager.providers = original


def test_select_still_returns_highest_priority_provider():
    manager = ProviderManager()
    original = dict(manager.providers)

    try:
        manager.providers = {
            "LOW": replace(
                PROVIDERS["DUCKDUCKGO"],
                name="Low",
                priority=20,
            ),
            "HIGH": replace(
                PROVIDERS["DUCKDUCKGO"],
                name="High",
                priority=10,
            ),
        }

        assert manager.select("SEARCH") is manager.providers["HIGH"].instance
    finally:
        manager.providers = original
