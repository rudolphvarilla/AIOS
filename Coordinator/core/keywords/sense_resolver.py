"""
===========================================================
AIOS Lexical Sense Resolver
core/keywords/sense_resolver.py
===========================================================

Resolves ambiguous keyword matches using already-extracted semantic intent.

This is deterministic. It does not call an LLM and it does not invent a new
meaning. It only reweights candidate registry matches when the user context
strongly supports one sense over another.

Version 1.0
===========================================================
"""


class SenseResolver:

    # Only genuinely ambiguous high-impact terms belong here. New terms can be
    # added as the system encounters them; ordinary keywords require no entry.
    AMBIGUOUS = {
        "current": {
            "time": {"time", "temporal", "weather", "travel"},
            "engineering": {"engineering", "physics", "electrical", "fluid"},
        },
        "present": {
            "time": {"time", "temporal", "weather", "travel"},
        },
        "flow": {
            "engineering": {"engineering", "physics", "fluid", "electrical"},
            "time": {"time", "temporal"},
        },
    }

    def adjust(self, match, semantic, text=""):
        keyword = match.get("matched", "").casefold()
        senses = self.AMBIGUOUS.get(keyword)

        if not senses:
            return match

        domains = {
            str(value).casefold()
            for value in getattr(semantic, "domains", [])
        }
        concepts = {
            str(value).casefold()
            for value in getattr(semantic, "concepts", [])
        }
        intent = str(
            getattr(semantic, "search_intent", "")
        ).casefold()
        context = " ".join(domains | concepts) + " " + intent + " " + text.casefold()

        domain = match.get("domain", "").casefold()

        positive = senses.get(domain, set())
        score = float(match.get("confidence", 1.0))

        for cue in positive:
            if cue in context:
                score *= 2.0

        # If another registered sense is explicitly represented by the
        # semantic intent, suppress an accidental keyword collision.
        for other_domain, cues in senses.items():
            if other_domain == domain:
                continue
            if any(cue in context for cue in cues):
                score *= 0.25
                break

        match = dict(match)
        match["confidence"] = score
        match["sense_resolved"] = bool(domains or concepts or intent)
        return match
