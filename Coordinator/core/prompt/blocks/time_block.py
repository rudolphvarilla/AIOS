"""
===========================================================
AIOS Time Prompt Block
core/prompt/blocks/time_block.py
===========================================================

Injects current date and time into the prompt.

This provides temporal awareness to the language model.

Future

• Timezone
• Relative time
• User locale
• Travel time
===========================================================
"""


class TimeBlock:

    def enabled(self, state):

        return True

    def build(self, state):

        prompt = ""

        prompt += (
            "CURRENT TIME\n"
            "--------------------\n"
        )

        prompt += f"Date      : {state.time.date()}\n"
        prompt += f"Time      : {state.time.time()}\n"
        prompt += f"Weekday   : {state.time.weekday()}\n"

        return prompt