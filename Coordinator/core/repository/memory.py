"""
Repository Memory Module
/core/repository/memory.py

Temporary wrapper around the current MemoryManager.

Later this becomes one component of the Information Repository.
"""

from core.memory.manager import MemoryManager


class MemoryModule(MemoryManager):

    def __init__(self, time):

        super().__init__(time)