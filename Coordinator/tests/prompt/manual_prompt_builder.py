from types import SimpleNamespace

from core.prompt.builder import PromptBuilder

builder = PromptBuilder()

state = SimpleNamespace(
    user_input="Explain Bernoulli's Principle.",
    search_results=[
        {
            "title": "Wikipedia",
            "url": "https://wikipedia.org",
            "snippet": "Bernoulli's principle states...",
        },
        {
            "title": "Science Notes",
            "url": "https://sciencenotes.org",
            "snippet": "Pressure decreases...",
        },
    ],
    plan=None,
    decision=None,
)

prompt = builder.build(state)

print()
print("=" * 50)
print(prompt)
