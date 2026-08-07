"""
===========================================================
AIOS Search Pipeline
core/search/pipeline.py
===========================================================

Central search processing pipeline.

Version 1.3 - Phase 3.1.15 deterministic fact extraction
===========================================================
"""

from core.search.authority import AuthorityScorer
from core.search.ranker import SearchRanker
from core.search.deduplicator import SearchDeduplicator
from core.search.summarizer import SearchSummarizer
from core.search.filter import SearchFilter
from core.search.extractor import SearchExtractor
from core.search.fact_extractor import SearchFactExtractor
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
        self.fact_extractor = SearchFactExtractor()
        self.normalizer = SearchNormalizer()
        self.classifier = SearchEntityClassifier()
        self.linker = EntityLinker()
        self.context_builder = SearchContextBuilder()
        self.evaluator = SearchEvaluator()
        self.enricher = SearchKnowledgeEnricher()

    def process(self, query, results, fivewh=None):

        self.authority.apply(results)

        print("\n===== RAW SEARCH RESULTS =====")
        if not results:
            print("No raw results returned.")

        for i, result in enumerate(results, start=1):
            print(f"\n[{i}]")
            print(f"Title   : {result.title}")
            print(f"URL     : {result.url}")
            print(f"Snippet : {result.snippet[:200]}")

        filtered = self.filter.filter(query, results)

        print("\n===== FILTERED RESULTS =====")
        if not filtered:
            print("No results survived filtering.")
        for i, result in enumerate(filtered, start=1):
            print(f"\n[{i}]")
            print(f"Title : {result.title}")
            print(f"URL   : {result.url}")

        print(f"\n[PIPELINE] Raw Results      : {len(results)}")
        print(f"[PIPELINE] Filtered Results : {len(filtered)}")

        ranked = self.ranker.rank(filtered)
        print(f"[PIPELINE] Ranked Results   : {len(ranked)}")

        print("\n===== RANKED RESULTS =====")
        for i, result in enumerate(ranked, start=1):
            print(f"\n[{i}]")
            print(f"Title : {result.title}")
            print(f"URL   : {result.url}")

        unique = self.deduplicator.deduplicate(ranked)
        print(f"[PIPELINE] Unique Results   : {len(unique)}")

        print("\n===== UNIQUE RESULTS =====")
        for i, result in enumerate(unique, start=1):
            print(f"\n[{i}]")
            print(f"Title : {result.title}")
            print(f"URL   : {result.url}")

        knowledge = self.extractor.extract(unique)
        knowledge.entities = self.normalizer.normalize(knowledge.entities)
        knowledge.entities = self.classifier.classify(knowledge.entities)

        knowledge.relations = self.linker.link(knowledge.entities)
        knowledge.fact_records = self.fact_extractor.extract(unique)
        knowledge.facts = [fact.render() for fact in knowledge.fact_records]
        knowledge = self.enricher.enrich(knowledge)

        print(f"[PIPELINE] Entities         : {len(knowledge.entities)}")
        print(f"[PIPELINE] Relations        : {len(knowledge.relations)}")
        print(f"[PIPELINE] Facts             : {len(knowledge.fact_records)}")

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

        summary = self.summarizer.summarize(
            query=query,
            results=unique,
        )

        print("\n===== SEARCH SUMMARY =====")
        print(summary)

        search_context = self.context_builder.build(
            query=query,
            results=unique,
            knowledge=knowledge,
            summary=summary,
            fivewh=fivewh,
        )

        print("\n===== SEARCH CONTEXT =====")
        print(search_context)

        search_evaluation = self.evaluator.evaluate_context(search_context)
        search_context.evaluation = search_evaluation

        print("\n===== SEARCH EVALUATION =====")
        print(f"Confidence          : {search_evaluation.confidence:.2f}")
        print(f"Entities            : {len(search_context.entities)}")
        print(f"Recommendations     : {len(search_context.recommendations)}")
        print(f"Facts               : {len(search_context.facts)}")
        print(f"5WH Score           : {search_evaluation.fivewh_score:.2f}")
        print(f"5WH Missing         : {search_evaluation.fivewh_missing}")
        print(f"Answerability       : {search_evaluation.answerability_score:.2f}")
        print(f"Answerability Missing: {search_evaluation.answerability_missing}")
        print(f"Retry               : {search_evaluation.should_retry}")
        print(f"Reason              : {search_evaluation.reason}")

        return (
            unique,
            knowledge,
            summary,
            search_context,
        )
