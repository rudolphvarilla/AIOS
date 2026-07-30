"""
===========================================================
AIOS Context Phase
core/execution/context_phase.py
===========================================================

Responsible for building semantic context.

Coordinator should never directly call ContextEngine.

===========================================================
"""

from core.context.engine import ContextEngine

_context_engine = ContextEngine()


def run(state):

    state.context = _context_engine.analyze(

        query=state.user_input,

        semantic=state.semantic,

    )

    return state