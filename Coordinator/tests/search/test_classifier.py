from core.search.knowledge import SearchEntity
from core.search.classifier import SearchEntityClassifier

classifier = SearchEntityClassifier()

entities = [

    SearchEntity("Tokyo", "", "unit"),

    SearchEntity("Japan", "", "unit"),

    SearchEntity("Aman Tokyo", "", "unit"),

    SearchEntity("Canon R6 Mark III", "", "unit"),

    SearchEntity("UGREEN DH4300", "", "unit"),

    SearchEntity("booking.com", "", "unit"),

    SearchEntity("Haneda Airport", "", "unit"),

]

result = classifier.classify(entities)

print("\n===== CLASSIFIED =====\n")

for entity in result:

    print(

        entity.name,

        "->",

        entity.entity_type

    )