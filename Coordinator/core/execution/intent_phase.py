"""
===========================================================
AIOS Intent Phase
core/execution/intent_phase.py
===========================================================

Responsible for intent classification.

===========================================================
"""

from core.intent.classifier import IntentClassifier

_classifier = IntentClassifier()


def run(state):

    state.intent_result = _classifier.classify(
        state.context
    )

    state.intent = state.intent_result.intent

    return state