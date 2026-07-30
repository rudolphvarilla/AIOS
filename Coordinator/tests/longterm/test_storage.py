from core.longterm.models import *
from core.longterm.storage import LongTermStorage

storage = LongTermStorage("data/test_memory.json")

entry = MemoryEntry(

    id="mem001",

    timestamp=current_timestamp(),

    title="Tokyo Hotel Preference",

    summary="User prefers Ueno area.",

    category=MemoryCategory.TRAVEL,

    importance=ImportanceLevel.HIGH,

    keywords=["tokyo", "hotel"],

)

storage.append(entry)

loaded = storage.load()

print()

print("===== LOADED =====")

print()

for item in loaded:

    print(item)