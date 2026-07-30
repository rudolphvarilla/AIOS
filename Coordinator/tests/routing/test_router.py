"""
AIOS Capability Router Tests

Verifies that the Capability Router
returns the correct execution strategy.

Version 1
"""

from core.routing.router import CapabilityRouter

router = CapabilityRouter()

tests = [
    ("GENERAL", "MEDIUM"),
    ("CODING", "LOW"),
    ("DOCUMENT", "LOW"),
    ("UNKNOWN", "LOW"),
]

for intent, complexity in tests:

    print("=" * 50)

    print(f"Intent      : {intent}")
    print(f"Complexity  : {complexity}")

    result = router.route(intent, complexity)

    print()

    print("Returned Route")

    print(f"Model Capability : {result['model_capability']}")
    print(f"Tool Capability  : {result['tool_capability']}")
    print(f"Memory           : {result['memory']}")
    print(f"Browser          : {result['browser']}")
    print(f"Vision           : {result['vision']}")
    print(f"Image Generation : {result['image_generation']}")

print("=" * 50)