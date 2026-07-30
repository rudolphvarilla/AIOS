"""
AIOS Working Memory
core/memory/working_memory.py

Stores the active operational context for the current execution.

Unlike Session Memory, Working Memory only contains the
information AIOS needs immediately.

Future versions will:
- Store execution context
- Track current objective
- Maintain active topic
- Interface with Memory Manager
"""

from dataclasses import dataclass, field


@dataclass
class WorkingMemory:

    time: object = field(repr=False)

    last_question: str = ""

    last_answer: str = ""

    current_topic: str = ""

    last_model: str = ""

    last_tool: str = ""

    last_complexity: str = ""

    timestamp: str = ""

    def update(self, state):

        self.last_question = state.user_input

        self.last_answer = state.response

        self.last_model = state.selected_model

        self.last_tool = str(state.selected_tool)

        self.last_complexity = state.plan.complexity

        self.timestamp = self.time.timestamp()

    def reset(self):

        self.last_question = ""
        self.last_answer = ""
        self.current_topic = ""
        self.last_model = ""
        self.last_tool = ""
        self.last_complexity = ""
        self.timestamp = ""