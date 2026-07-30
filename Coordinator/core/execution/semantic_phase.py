"""
===========================================================
AIOS Semantic Phase
core/execution/semantic_phase.py
===========================================================

Runs semantic understanding before Context Engine.

===========================================================
"""

from core.semantics.detector import SemanticDetector
from core.semantics.analysis import SemanticAnalysis

_detector = SemanticDetector()
_analysis = SemanticAnalysis()


def run(state):

    matches = _detector.detect(
        state.user_input
    )

    state.semantic = _analysis.analyze(matches)

    return state