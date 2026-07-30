"""
AIOS Service Registry

Registers all AIOS Services.

Services are responsible for orchestrating
Providers.

The Executor never communicates directly
with Providers.

Version 1
- Static registry
"""

from dataclasses import dataclass

from core.services.search.service import SearchService


@dataclass
class ServiceConfig:

    name: str

    capability: str

    available: bool

    description: str

    instance: object


SERVICES = {

    "Search": ServiceConfig(

        name="Search",

        capability="SEARCH",

        available=True,

        description="Internet Search Service",

        instance=SearchService()

    ),

}