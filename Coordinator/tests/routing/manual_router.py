from types import SimpleNamespace

from core.routing.router import CapabilityRouter

router = CapabilityRouter()

plans = [
    SimpleNamespace(
        model_capability="GENERAL",
        tool_capability=None,
        prompt_flags={},
        browser=False,
        vision=False,
        image_generation=False,
    ),
    SimpleNamespace(
        model_capability="CODING",
        tool_capability=None,
        prompt_flags={},
        browser=False,
        vision=False,
        image_generation=False,
    ),
    SimpleNamespace(
        model_capability="GENERAL",
        tool_capability="DOCUMENT_QA",
        prompt_flags={"memory": True},
        browser=False,
        vision=False,
        image_generation=False,
    ),
]

for plan in plans:
    result = router.route(plan)
    print("=" * 50)
    print("Returned Route")
    print(f"Model Capability : {result['model_capability']}")
    print(f"Tool Capability  : {result['tool_capability']}")
    print(f"Memory           : {result['memory']}")
    print(f"Browser          : {result['browser']}")
    print(f"Vision           : {result['vision']}")
    print(f"Image Generation : {result['image_generation']}")
