"""
===========================================================
AIOS User Prompt Block
core/prompt/blocks/user_block.py
===========================================================

Builds the user's current request.

Responsibilities

• Current User Question
• Input Formatting

This block is always the final context block before
the model begins generating a response.

Used by

• PromptBuilder

Future

- Multi-user Sessions
- Conversation Metadata
===========================================================
"""

class UserBlock:

    def enabled(self, state):

        return True

    def build(self, state):

        prompt = ""

        prompt += (
            "USER QUESTION\n"
            "--------------------\n"
        )

        prompt += state.user_input

        prompt += "\n\n"

        return prompt