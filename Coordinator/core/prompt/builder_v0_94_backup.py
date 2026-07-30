"""
AIOS Prompt Builder
Version 2

Constructs the final prompt sent to the selected model.

Every context source is assembled here into one unified prompt.

Context Sources
- User Question
- Working Memory
- Search Results

Future Versions
- Session Memory
- Qdrant Memory
- Workspace Context
- Knowledge Graph
- AIOS.md
- Tool Outputs
- Vision Context

built for AISO v0.9
"""


class PromptBuilder:

    def build(self, state):

        sections = []

        # ---------------------------------
        # User Question
        # ---------------------------------

        sections.append(
            self._build_user_question(state)
        )

        # ---------------------------------
        # Search Results
        # ---------------------------------

        if state.search_results:

            sections.append(
                self._build_search_results(state)
            )

        return "\n".join(sections)

    # ==================================================

    def _build_user_question(self, state):

        return (
            "USER QUESTION\n"
            "--------------------\n"
            f"{state.user_input}\n"
        )

    # ==================================================

    def _build_search_results(self, state):

        text = (
            "SEARCH RESULTS\n"
            "--------------------\n"
        )

        for i, result in enumerate(
            state.search_results,
            start=1
        ):

            text += (

                f"[{i}]\n"

                f"Title   : {result['title']}\n"

                f"URL     : {result['url']}\n"

                f"Snippet : {result['snippet']}\n\n"

            )

        return text