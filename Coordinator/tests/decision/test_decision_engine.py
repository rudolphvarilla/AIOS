from core.decision.engine import DecisionEngine

engine = DecisionEngine()

tests = [

    "What is 2+2?",

    "Latest Boeing news",

    "Current weather in Manila",

    "Write a Python factorial function",

    "Explain Bernoulli's Principle",

]

for question in tests:

    decision = engine.decide(question)

    print("=" * 60)

    print(question)

    print(decision)