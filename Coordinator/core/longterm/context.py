from dataclasses import dataclass, field

@dataclass
class RetrievedMemory:

    memory: object

    reason: str

    confidence: float


@dataclass
class LongTermContext:

    summary: str = ""

    retrieved: list[RetrievedMemory] = field(default_factory=list)