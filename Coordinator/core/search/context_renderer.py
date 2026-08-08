"""
===========================================================
AIOS Search Context Renderer
core/search/context_renderer.py
===========================================================

Converts SearchContext into prompt text.

No search logic belongs here.

Version 1.2 - source-grounded fact constraints
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
                lines.append(f"- {recommendation}")
            lines.append("")

        if context.fact_records:
            lines.append("SOURCE-GROUNDED FACTS")
            lines.append("--------------------")
            lines.append(
                "Use these records as the factual boundary for search-derived claims."
            )
            lines.append(
                "Values and statements are copied from retrieved source text;"
            )
            lines.append(
                "do not upgrade qualifiers, infer unstated causes, or replace unfamiliar"
            )
            lines.append(
                "terminology with an interpretation unless the source explicitly supports it."
            )
            lines.append("")

            for fact in context.fact_records:
                lines.append(f"- TYPE: {fact.fact_type}")
                lines.append(f"  SUBJECT: {fact.subject}")
                lines.append(f"  PREDICATE: {fact.predicate}")
                lines.append(f"  VALUE: {fact.value}")
                lines.append(f"  EVIDENCE: {fact.evidence}")
                lines.append(f"  SOURCE: {fact.source}")
                lines.append(f"  CONFIDENCE: {fact.confidence:.2f}")
                lines.append("")

            lines.append(
                "FACT RESPONSE RULE: distinguish what the source states from what"
            )
            lines.append(
                "you infer. Preserve epistemic wording such as may, could, likely,"
            )
            lines.append(
                "possible, reported, expected, or according to the source."
            )
            lines.append("")

        if context.sources:
            lines.append("Sources")
            for source in context.sources:
                lines.append(f"- {source}")
            lines.append("")

        lines.append(f"Confidence : {context.confidence:.2f}")

        return "\n".join(lines)
