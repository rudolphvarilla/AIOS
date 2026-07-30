"""
===========================================================
AIOS Perception Engine
core/perception/engine.py
===========================================================

Collects raw observations before routing.

Responsibilities

• Entity Detection
• Requirement Detection
• Repository Detection
• Confidence Estimation

Produces a unified PerceptionResult.

Version 1.0
===========================================================
"""

from core.perception.result import PerceptionResult

from core.perception.analyzers.entity_detector import EntityDetector
from core.perception.analyzers.requirement_detector import RequirementDetector
from core.perception.analyzers.repository_detector import RepositoryDetector
from core.perception.analyzers.confidence import ConfidenceAnalyzer


class PerceptionEngine:

    def __init__(self):

        self.entity_detector = EntityDetector()

        self.requirement_detector = RequirementDetector()

        self.repository_detector = RepositoryDetector()

        self.confidence_analyzer = ConfidenceAnalyzer()

    def analyze(self, text):

        result = PerceptionResult()

        # ---------------------------------
        # Entity Detection
        # ---------------------------------

        result.entities = self.entity_detector.detect(text)

        # ---------------------------------
        # Requirement Detection
        # ---------------------------------

        result.requirements = self.requirement_detector.detect(text)

        # ---------------------------------
        # Repository Detection
        # ---------------------------------

        result.repository_targets = (
            self.repository_detector.detect(text)
        )

        # ---------------------------------
        # Confidence
        # ---------------------------------

        result.confidence = (
            self.confidence_analyzer.compute(result)
        )

        return result