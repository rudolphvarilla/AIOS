"""
AIOS Tool Manager Tests

Verifies that the Tool Registry and Tool Manager
correctly discover registered tools.

Version 1:
- Registry validation
- Tool selection
"""

from core.tools.manager import ToolManager


manager = ToolManager()

print("=" * 40)
print("AVAILABLE TOOLS")
print("=" * 40)

for tool in manager.list_tools():

    print(tool)

print()

print("=" * 40)
print("EXISTS TEST")
print("=" * 40)

print(manager.exists("AnythingLLM"))
print(manager.exists("Browser"))

print()

print("=" * 40)
print("GET TEST")
print("=" * 40)

print(manager.get("AnythingLLM"))

print()

print("=" * 40)
print("SELECT TEST")
print("=" * 40)

tool = manager.select("DOCUMENT_QA")

print(tool)