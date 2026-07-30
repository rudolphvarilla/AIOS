from core.longterm.manager import LongTermMemoryManager
from core.longterm.models import *
from core.longterm.retrieval import LongTermRetrieval

manager = LongTermMemoryManager()

manager.save(

    manager.create(

        title="Tokyo Hotel",

        summary="User prefers staying near Ueno.",

        category=MemoryCategory.TRAVEL,

        importance=ImportanceLevel.HIGH,

        keywords=[

            "tokyo",

            "hotel",

            "ueno",

        ],

    )

)

manager.save(

    manager.create(

        title="Canon Camera",

        summary="User shoots RAW using Canon.",

        category=MemoryCategory.PHOTOGRAPHY,

        importance=ImportanceLevel.MEDIUM,

        keywords=[

            "canon",

            "camera",

            "raw",

        ],

    )

)

retrieval = LongTermRetrieval()

results = retrieval.retrieve(

    "tokyo hotel"

)

print()

print("===== RETRIEVED =====")

print()

for memory in results:

    print(memory.title)