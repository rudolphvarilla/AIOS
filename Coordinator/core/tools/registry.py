"""
AIOS Tool Registry

Central registry of every external capability
available to AIOS.

This registry does not execute tools.

It only describes what tools exist and what
capability each provides.

Version 1:
- Static registry
- Local tools only
"""

from core.tools.base import ToolConfig

TOOLS = {

    "AnythingLLM": ToolConfig(
        name="AnythingLLM",
        capability="DOCUMENT_QA",
        available=False,
        description="Document Retrieval"
    ),

    "Qdrant": ToolConfig(
        name="Qdrant",
        capability="SEMANTIC_MEMORY",
        available=False,
        description="Long-term semantic memory"
    ),

    "Graphify": ToolConfig(
        name="Graphify",
        capability="KNOWLEDGE_GRAPH",
        available=False,
        description="Knowledge graph extraction"
    ),

}