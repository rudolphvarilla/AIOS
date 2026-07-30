"""
===========================================================
AIOS Entity Linker
core/search/linker.py
===========================================================

Creates relationships between extracted entities.

Version 2.0
===========================================================
"""

from core.search.knowledge import SearchRelation


class EntityLinker:

    def link(self, entities):

        relations = []

        names = {

            entity.name

            for entity in entities

        }

        # ---------------------------------
        # Example rules
        # ---------------------------------

        if "Tokyo" in names and "Japan" in names:

            relations.append(

                SearchRelation(

                    source="Tokyo",

                    relation="LOCATED_IN",

                    target="Japan",

                )

            )

        if "Aman Tokyo" in names and "Tokyo" in names:

            relations.append(

                SearchRelation(

                    source="Aman Tokyo",

                    relation="LOCATED_IN",

                    target="Tokyo",

                )

            )

        if "Haneda Airport" in names and "Tokyo" in names:

            relations.append(

                SearchRelation(

                    source="Haneda Airport",

                    relation="LOCATED_IN",

                    target="Tokyo",

                )

            )

        return relations