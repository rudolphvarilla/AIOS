"""
===========================================================
AIOS Memory Manager
core/memory/manager.py
===========================================================

Coordinates every memory subsystem.

Acts as the single interface between AIOS and all memory layers.

Future versions will coordinate:

• Working Memory
• Session Memory
• Long-Term Memory
• Knowledge Graph
• Qdrant
===========================================================
"""

print("Loading MemoryManager from:", __file__)

from core.memory.working_memory import WorkingMemory
from core.memory.session_memory import SessionMemory


class MemoryManager:

    def __init__(self, time):

        self.time = time

        self.working = WorkingMemory(time)

        self.session = SessionMemory(time)

    def commit(self, state):

        self.working.update(state)

        self.session.add(state)