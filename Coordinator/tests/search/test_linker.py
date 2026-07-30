from core.search.linker import EntityLinker
from core.search.knowledge import SearchEntity

entities = [

    SearchEntity("Tokyo", "CITY", "search"),

    SearchEntity("Japan", "COUNTRY", "search"),

    SearchEntity("Aman Tokyo", "HOTEL", "search"),

]

linker = EntityLinker()

relations = linker.link(entities)

print()

print("===== RELATIONS =====")

print()

for relation in relations:

    print(

        relation.source,

        relation.relation,

        relation.target,

    )