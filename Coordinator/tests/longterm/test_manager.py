from core.longterm.manager import LongTermMemoryManager
from core.longterm.models import *

manager = LongTermMemoryManager()

memory = manager.create(

    title="Tokyo Hotel",

    summary="User prefers Ueno area.",

    category=MemoryCategory.TRAVEL,

    importance=ImportanceLevel.HIGH,

    keywords=[

        "tokyo",

        "hotel",

        "ueno",

    ],

)

manager.save(memory)

print()

print("===== CREATED =====")

print(memory)

print()

print("===== LOADED =====")

for item in manager.load_all():

    print(item)