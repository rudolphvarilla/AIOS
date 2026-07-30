"""
===========================================================
AIOS Perception Regression Tests
tests/perception/test_perception.py
===========================================================

Regression tests for the Perception subsystem.

Tasks Covered

50.2.2  Entity Detector
50.2.4  Requirement Detector
50.2.5  Repository Detector
50.2.6  Confidence Analyzer
50.2.3  Perception Engine

Run

python tests/test_perception.py
===========================================================
"""

from core.perception.engine import PerceptionEngine
from core.perception.analyzers.entity_detector import EntityDetector
from core.perception.analyzers.requirement_detector import RequirementDetector
from core.perception.analyzers.repository_detector import RepositoryDetector


def divider(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ----------------------------------------------------------
# Entity Detector
# ----------------------------------------------------------

divider("Entity Detector")

entity = EntityDetector()

queries = [

    "best hotels in tokyo",

    "python reverse string",

    "lift drag thrust",

    "dragon",

]

for q in queries:

    print(q)

    print(entity.detect(q))

    print()


# ----------------------------------------------------------
# Requirement Detector
# ----------------------------------------------------------

divider("Requirement Detector")

requirement = RequirementDetector()

queries = [

    "best hotels in tokyo",

    "compare synology vs ugreen",

    "explain lift equation",

    "calculate wing loading",

    "remember my favorite color",

    "book hotel",

]

for q in queries:

    print(q)

    print(requirement.detect(q))

    print()


# ----------------------------------------------------------
# Repository Detector
# ----------------------------------------------------------

divider("Repository Detector")

repository = RepositoryDetector()

queries = [

    "remember my favorite color",

    "explain lift equation",

    "schedule my flight",

    "monitor flights to japan",

    "my friend john",

]

for q in queries:

    print(q)

    print(repository.detect(q))

    print()


# ----------------------------------------------------------
# Perception Engine
# ----------------------------------------------------------

divider("Perception Engine")

engine = PerceptionEngine()

queries = [

    "best hotels in tokyo",

    "python reverse string",

    "calculate lift",

    "remember my favorite color",

    "monitor flights to japan",

]

for q in queries:

    print(q)

    print(engine.analyze(q))

    print()

print("\nPerception regression complete.")