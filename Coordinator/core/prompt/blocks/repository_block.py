"""
===========================================================
AIOS Repository Prompt Block
core/prompt/blocks/repository_block.py
===========================================================

Provides the language model awareness of the AIOS
Information Repository.

Version 2
===========================================================
"""


class RepositoryBlock:

    def enabled(self, state):
        return True

    def build(self, state):

        repo = state.repository

        sections = [

            "INFORMATION REPOSITORY",
            "--------------------",

            f"Memory Module        : {type(repo.memory).__name__}",
            f"Knowledge Module     : {type(repo.knowledge).__name__}",
            f"Event Module         : {type(repo.events).__name__}",
            f"Relationship Module  : {type(repo.relationships).__name__}",
            f"Watcher Module       : {type(repo.watchers).__name__}",

        ]

        return "\n".join(sections)