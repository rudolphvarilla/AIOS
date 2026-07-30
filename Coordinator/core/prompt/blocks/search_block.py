"""
===========================================================
AIOS Search Prompt Block
core/prompt/blocks/search_block.py
===========================================================

Renders Search Context into the final prompt.

The Prompt Block knows nothing about Search Pipeline internals.

Version 3.0
===========================================================
"""

from core.search.context_renderer import SearchContextRenderer


class SearchBlock:

    def __init__(self):

        self.renderer = SearchContextRenderer()

    # -------------------------------------------------

    def build(

        self,

        state,

    ):

        if state.search_context is None:

            return ""

        return self.renderer.render(

            state.search_context

        )