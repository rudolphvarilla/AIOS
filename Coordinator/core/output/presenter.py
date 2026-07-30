"""
===========================================================
AIOS Output Presenter
core/output/presenter.py
===========================================================

Responsible for all user-visible output.

Responsibilities

• AI response
• Developer output delegation

Coordinator should never print directly.

Version 1.0
===========================================================
"""

from core.output.developer_output import DeveloperOutput


class Presenter:

    def __init__(self):

        self.developer_output = DeveloperOutput()

    def present(

        self,

        state,

        developer,

        memory,

        scheduler,

        performance,

    ):

        # -------------------------
        # Normal response
        # -------------------------

        print("\n----- RESPONSE -----")

        print(state.response)

        print()

        # -------------------------
        # Developer output
        # -------------------------

        if developer.enabled:

            self.developer_output.present(

                state=state,

                memory=memory,

                scheduler=scheduler,

                perf=performance,

            )