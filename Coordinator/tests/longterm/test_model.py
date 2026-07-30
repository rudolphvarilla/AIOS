from core.longterm.models import *

entry = MemoryEntry(

    id="mem001",

    timestamp=current_timestamp(),

    title="Tokyo Hotel Preference",

    summary="User prefers Ueno area.",

    category=MemoryCategory.TRAVEL,

    importance=ImportanceLevel.HIGH,

    keywords=["tokyo", "hotel", "ueno"]

)

print(entry)