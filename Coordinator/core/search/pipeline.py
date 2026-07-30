"""
===========================================================
AIOS Search Pipeline
core/search/pipeline.py
===========================================================

Central search processing pipeline.

Flow

Provider
    ↓
Authority
    ↓
Ranker
    ↓
Deduplicator
    ↓
Summarizer

Version 1.0
===========================================================
"""

from core.search.authority import AuthorityScorer
from core.search.ranker import SearchRanker
from core.search.deduplicator import SearchDeduplicator
from core.search.summarizer import SearchSummarizer
from core.search.filter import SearchFilter
from core.search.extractor import SearchExtractor
from core.search.normalizer import SearchNormalizer
from core.search.classifier import SearchEntityClassifier
from core.search.linker import EntityLinker
from core.search.search_context import SearchContextBuilder
from core.search.enricher import SearchKnowledgeEnricher
from core.search.evaluator import SearchEvaluator

class SearchPipeline:

    def __init__(self):
        self.authority = AuthorityScorer()
        self.ranker = SearchRanker()
        self.deduplicator = SearchDeduplicator()
        self.summarizer = SearchSummarizer()
        self.filter = SearchFilter()
        self.extractor = SearchExtractor()
        self.normalizer = SearchNormalizer()
        self.classifier = SearchEntityClassifier()
        self.linker = EntityLinker()
        self.context_builder = SearchContextBuilder()
        self.evaluator = SearchEvaluator()
        self.enricher = SearchKnowledgeEnricher()

    # -------------------------------------------------

    def process(
        self,
        query,
        results,
    ):

        # ---------------------------------
        # Authority
        # ---------------------------------

        self.authority.apply(results)

        # ---------------------------------
        # Debug mode - Show Raw Results
        # ---------------------------------

        print("\n===== RAW SEARCH RESULTS =====")

        if not results:
            print("No raw results returned.")

        for i, result in enumerate(results, start=1):

            print(f"\n[{i}]")

            print(f"Title   : {result.title}")

            print(f"URL     : {result.url}")

            print(f"Snippet : {result.snippet[:200]}")

        # ---------------------------------
        # Filter
        # ---------------------------------

        filtered = self.filter.filter(
            query,
            results,
        )

        print("\n===== FILTERED RESULTS =====")

        # ---------------------------------
        # Debug mode - Show Filtered Results
        # ---------------------------------

        if not filtered:
            print("No results survived filtering.")
        for i, result in enumerate(filtered, start=1):
            print(f"\n[{i}]")
            print(f"Title : {result.title}")
            print(f"URL   : {result.url}")

        # End Debug Mode ------------------

        print(f"\n[PIPELINE] Raw Results      : {len(results)}")
        print(f"[PIPELINE] Filtered Results : {len(filtered)}")

        # ---------------------------------
        # Rank
        # ---------------------------------

        ranked = self.ranker.rank(filtered)

        print(f"[PIPELINE] Ranked Results   : {len(ranked)}")

        # ---------------------------------
        # Debug mode - Show Ranking
        # ---------------------------------

        print("\n===== RANKED RESULTS =====")

        for i, result in enumerate(ranked, start=1):

            print(f"\n[{i}]")

            print(f"Title : {result.title}")

            print(f"URL   : {result.url}")

        # ---------------------------------
        # Deduplicate
        # ---------------------------------

        unique = self.deduplicator.deduplicate(ranked)

        print(f"[PIPELINE] Unique Results   : {len(unique)}")

        # ---------------------------------
        # Debug mode - Show Deduplicates? or what?
        # ---------------------------------

        print("\n===== UNIQUE RESULTS =====")

        for i, result in enumerate(unique, start=1):

            print(f"\n[{i}]")

            print(f"Title : {result.title}")

            print(f"URL   : {result.url}")

        # ---------------------------------
        # Extract Knowledge
        # ---------------------------------

        knowledge = self.extractor.extract(unique)

        knowledge.entities = self.normalizer.normalize(knowledge.entities)

        knowledge.entities = self.classifier.classify(knowledge.entities)

        print(f"[PIPELINE] Entities         : {len(knowledge.entities)}")
        print(f"[PIPELINE] Relations        : {len(knowledge.relations)}")

        # ---------------------------------
        # Link Entities
        # ---------------------------------

        knowledge.relations = self.linker.link(knowledge.entities)

        knowledge = self.enricher.enrich(knowledge)

        print("\n===== ENRICHED KNOWLEDGE =====")

        print("\nRecommendations")
        for item in knowledge.recommendations:
            print(" -", item)

        print("\nCategories")
        for key, value in knowledge.categories.items():
            print(f"{key}: {value}")

        print("\nLocations")
        for location in knowledge.locations:
            print(" -", location)

        print("\nAttributes")
        for attribute in knowledge.attributes:
            print(" -", attribute)

        print("\nFacts")
        for fact in knowledge.facts:
            print(" -", fact)

        # ---------------------------------
        # Summarize
        # ---------------------------------

        summary = self.summarizer.summarize(
            query=query,
            results=unique,
        )

        # ---------------------------------
        # Debug mode - Show Summary
        # ---------------------------------

        print("\n===== SEARCH SUMMARY =====")
        print(summary)

        # ---------------------------------
        # Build Search Context
        # ---------------------------------

        search_context = self.context_builder.build(
            query=query,
            results=unique,
            knowledge=knowledge,
            summary=summary,
        )

        print("\n===== SEARCH CONTEXT =====")

        print(search_context)

        # ---------------------------------
        # Evaluate Search Context
        # ---------------------------------

        search_evaluation = self.evaluator.evaluate_context(
            search_context
        )

        search_context.evaluation = search_evaluation

        # ---------------------------------
        # Debug mode - Show Summary
        # ---------------------------------

        print("\n===== SEARCH EVALUATION =====")

        print(f"Confidence       : {search_evaluation.confidence:.2f}")
        print(f"Entities         : {len(search_context.entities)}")
        print(f"Recommendations  : {len(search_context.recommendations)}")
        print(f"Facts            : {len(search_context.facts)}")
        print(f"Retry            : {search_evaluation.should_retry}")
        print(f"Reason           : {search_evaluation.reason}")

        # ---------------------------------
        # Return
        # ---------------------------------

        return (
            unique,
            knowledge,
            summary,
            search_context,
        )