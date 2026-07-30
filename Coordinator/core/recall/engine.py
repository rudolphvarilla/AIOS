"""
AIOS Recall Engine

Determines whether previous memory should be
used before executing the current request.

Version 1:
- Working Memory only
- No Session search
- No Qdrant
- No AI reasoning
"""

FOLLOW_UP_WORDS = {
    "it",
    "that",
    "this",
    "those",
    "these",
    "derive",
    "continue",
    "expand",
    "elaborate",
    "more",
    "equation",
    "proof",
}


def should_recall(question):
    """
    Returns True if the question appears to be
    a follow-up to the previous conversation.
    """

    question = question.lower()

    words = question.split()

    for word in words:

        if word in FOLLOW_UP_WORDS:

            return True

    return False


def build_context(memory):
    """
    Builds the context that will eventually
    be injected into the model prompt.
    """

    working = memory.working

    if not working.last_question:

        return ""

    context = (
        f"Previous question:\n"
        f"{working.last_question}\n\n"
        f"Previous answer:\n"
        f"{working.last_answer}"
    )

    return context


def recall(question, memory):
    """
    Main Recall Engine entry point.
    """

    if not should_recall(question):

        return ""

    return build_context(memory)