"""
AIOS Capability Registry

The Planner never selects a model directly.

Instead, it selects a capability.

The Executor consults this registry to determine
which model and tool should satisfy that capability.
"""

REGISTRY = {

    "GENERAL": {
        "tool": None,
        "description": "Fast everyday conversation and general knowledge"
    },

    "CODING": {
        "tool": None,
        "description": "Programming, debugging and software engineering"
    },

    "DOCUMENT_QA": {
        "tool": "AnythingLLM",
        "description": "Question answering over uploaded documents"
    },

    "SEMANTIC_MEMORY": {
        "tool": "Qdrant",
        "description": "Retrieve and summarize semantic memories"
    },

    "KNOWLEDGE_GRAPH": {
        "tool": "Graphify",
        "description": "Graph extraction and repository understanding"
    }

}