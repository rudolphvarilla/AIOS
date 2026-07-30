from core.search.knowledge import SearchEntity
from core.search.normalizer import SearchNormalizer

normalizer = SearchNormalizer()

entities = [

    SearchEntity(
        name="THE",
        entity_type="UNKNOWN",
        source="unit"
    ),

    SearchEntity(
        name="BEST Hotels",
        entity_type="UNKNOWN",
        source="unit"
    ),

    SearchEntity(
        name="Tokyo",
        entity_type="CITY",
        source="unit"
    ),

    SearchEntity(
        name="Tokyo",
        entity_type="CITY",
        source="unit"
    ),

    SearchEntity(
        name="Aman Tokyo",
        entity_type="HOTEL",
        source="unit"
    ),

]

result = normalizer.normalize(entities)

print("\n===== NORMALIZED =====\n")

for entity in result:

    print(entity.name)