"""
AIOS Registry

Contains every model and tool currently installed.
The router consults this registry when selecting which component to use.
"""

MODELS = {
    "DEEP_REASONING": "qwen3:8b",
    "FAST_GENERAL" : "qwen3:4b",
    "coding": "qwen2.5-coder:3b",
}

TOOLS = {
    "documents": "AnythingLLM",
    "memory": "Qdrant",
    "knowledge_graph": "Graphify",
}