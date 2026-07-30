"""
===========================================================
AIOS Semantic Analysis
core/semantics/analysis.py
===========================================================

Converts detected semantic signals into a usable summary
for the planner.

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field

from core.semantics.detector import SemanticDetector


@dataclass
class SemanticAnalysis:

    # main topic
    primary_topic: str | None = None

    # detected intents
    intents: list[str] = field(default_factory=list)

    # detected entities
    entities: list[str] = field(default_factory=list)

    # planner hints
    requires_search: bool = False
    requires_memory: bool = False
    requires_repository: bool = False
    requires_time: bool = False
    requires_reasoning: bool = False

    confidence: float = 0.0


class SemanticAnalysisEngine:

    def __init__(self):

        self.detector = SemanticDetector()

    def analyze(self, user_input):

        detection = self.detector.detect(user_input)

        result = SemanticAnalysis()

        result.primary_topic = detection.primary_topic
        result.intents = detection.intents
        result.entities = detection.entities

        # ----------------------------
        # Planner hints
        # ----------------------------

        intents = set(detection.intents)

        if "SEARCH" in intents:
            result.requires_search = True

        if "MEMORY" in intents:
            result.requires_memory = True

        if "TIME" in intents:
            result.requires_time = True

        if "REPOSITORY" in intents:
            result.requires_repository = True

        # reasoning required whenever
        # there is at least one semantic intent

        result.requires_reasoning = len(intents) > 0

        # ----------------------------
        # Confidence
        # ----------------------------

        score = 0.30

        if result.primary_topic:
            score += 0.20

        score += min(len(result.intents), 3) * 0.15
        score += min(len(result.entities), 5) * 0.04

        result.confidence = min(score, 1.0)

        return result