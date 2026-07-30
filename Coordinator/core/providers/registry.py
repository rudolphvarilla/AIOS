"""
AIOS Provider Registry

Defines every external provider
available to AIOS.

Providers perform work for Services.

Version 1
"""

from dataclasses import dataclass
from core.providers.duckduckgo import DuckDuckGoProvider

@dataclass
class ProviderConfig:

    name: str

    service: str

    priority: int

    available: bool

    requires_api: bool

    description: str

    instance: object


PROVIDERS = {

    "DUCKDUCKGO": ProviderConfig(

        name="DuckDuckGo",

        service="SEARCH",

        priority=1,

        available=True,

        requires_api=False,

        description="Free internet search",

        instance=DuckDuckGoProvider()

    ),

    "BRAVE": ProviderConfig(

        name="Brave Search",

        service="SEARCH",

        priority=2,

        available=False,

        requires_api=True,

        description="Brave Search API",

        instance=None

    ),

    "GOOGLE": ProviderConfig(

        name="Google Search",

        service="SEARCH",

        priority=3,

        available=False,

        requires_api=True,

        description="Google Custom Search API",

        instance=None

    ),

    "SEARXNG": ProviderConfig(

        name="SearXNG",

        service="SEARCH",

        priority=4,

        available=False,

        requires_api=False,

        description="Self-hosted search engine",

        instance=None

    ),

    "TAVILY": ProviderConfig(

        name="Tavily",

        service="SEARCH",

        priority=5,

        available=False,

        requires_api=True,

        description="AI research search",

        instance=None

    ),

}