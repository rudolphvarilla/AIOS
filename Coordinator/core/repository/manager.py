"""
AIOS Information Repository
core/repository/manager.py

Central access point for all information stored by AIOS.

Everything above this layer communicates ONLY through the repository.

Future modules:
- Memory
- Knowledge
- Events
- Relationships
- Watchers
"""

from core.repository.memory import MemoryModule
from core.repository.knowledge import KnowledgeModule
from core.repository.events import EventModule
from core.repository.relationship import RelationshipModule
from core.repository.watchers import WatcherModule


class RepositoryManager:

    def __init__(self, time):

        self.memory = MemoryModule(time)

        self.knowledge = KnowledgeModule()

        self.events = EventModule()

        self.relationships = RelationshipModule()

        self.watchers = WatcherModule()