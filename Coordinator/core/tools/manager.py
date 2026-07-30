"""
AIOS Tool Manager

Selects external tools required by the Planner.

The Executor never searches for tools directly.

Instead, it asks the Tool Manager to locate
the best registered tool for a requested capability.

Version 1:
- Static registry
- Capability selection
- Availability checking
"""

from core.tools.registry import TOOLS

class ToolManager:

    def __init__(self):

        self.tools = TOOLS

    #--------------------
    # Register Tool
    #--------------------

    def register(self, name, config):

        self.tools[name] = config

    #--------------------
    # Get Tool
    #--------------------

    def get(self, name):

        return self.tools.get(name)

    #--------------------
    # Check tool if exists
    #--------------------

    def exists(self, name):

        return name in self.tools

    #--------------------
    # List tools
    #--------------------

    def list_tools(self):

        return list(self.tools.keys())

    #--------------------
    # Select tool
    #--------------------

    def select(self, capability):

        for tool in self.tools.values():

            if not tool.available:

                continue

            if tool.capability == capability:

                return tool

        return None

"""
    #debug mode
    #open cmd in coordinator folder. type: python -m tests.test_tools
    output will look like this:

========================================
AVAILABLE TOOLS
========================================
AnythingLLM
Qdrant
Graphify

========================================
EXISTS TEST
========================================
True
False

========================================
GET TEST
========================================
ToolConfig(name='AnythingLLM', capability='DOCUMENT_QA', available=False, description='Document Retrieval')

========================================
SELECT TEST
========================================

Selecting tool...
Requested Capability : DOCUMENT_QA
Checking -> AnythingLLM | DOCUMENT_QA
Checking -> Qdrant | SEMANTIC_MEMORY
Checking -> Graphify | KNOWLEDGE_GRAPH
No matching tool found.
None



    def select(self, capability):

        print("\nSelecting tool...")
        print(f"Requested Capability : {capability}")

        for tool in self.tools.values():

            print(
                f"Checking -> {tool.name} | "
                f"{tool.capability}"
            )

            if not tool.available:

                continue

            if tool.capability == capability:

                print(f"Selected -> {tool.name}")

                return tool

        print("No matching tool found.")

        return None
"""