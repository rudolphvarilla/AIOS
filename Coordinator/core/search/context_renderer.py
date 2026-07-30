"""
===========================================================
AIOS Search Context Renderer
core/search/context_renderer.py
===========================================================

Converts SearchContext into prompt text.

No search logic belongs here.

Version 1.0
===========================================================
"""


class SearchContextRenderer:

    def render(

        self,

        context,

    ):

        if context is None:

            return ""

        lines = []

        lines.append("SEARCH CONTEXT")

        lines.append("--------------------")

        lines.append(f"Topic : {context.topic}")

        lines.append("")

        lines.append("Summary")

        lines.append(context.summary)

        lines.append("")

        if context.entities:

            lines.append("Entities")

            for entity in context.entities:

                lines.append(

                    f"- {entity.name} ({entity.entity_type})"

                )

            lines.append("")

        if context.relations:

            lines.append("Relationships")

            for relation in context.relations:

                lines.append(

                    f"- {relation.source} {relation.relation} {relation.target}"

                )

            lines.append("")

        if context.recommendations:

            lines.append("Recommendations")

            for recommendation in context.recommendations:

                lines.append(

                    f"- {recommendation}"

                )

            lines.append("")

        if context.sources:

            lines.append("Sources")

            for source in context.sources:

                lines.append(

                    f"- {source}"

                )

            lines.append("")

        lines.append(

            f"Confidence : {context.confidence:.2f}"

        )

        return "\n".join(lines)