"""
===========================================================
AIOS Travel Keyword Registry
core/keywords/registries/travel.py
===========================================================

Semantic Registry v2

Instead of storing individual keywords, AIOS stores
canonical concepts.

Each concept owns a collection of keywords.

Future versions may automatically expand these keyword
collections through the Semantic Evolution Engine.

Version 2
===========================================================
"""

TRAVEL = {

    "travel": {
        "keywords": {
            "travel","trip","vacation","holiday","tour",
            "tourism","tourist","journey","visit"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "planning": {
        "keywords":{
            "itinerary",
            "booking",
            "destination",
            "schedule",
            "travel plan",
            "travel planning",
            "route",
            "reservation"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "hotel":{
        "keywords":{
            "hotel",
            "hostel",
            "resort",
            "airbnb",
            "accommodation",
            "guesthouse",
            "check in",
            "check out"
            "hotel check in",
            "hotel check out"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "airport":{
        "keywords":{
            "airport",
            "terminal",
            "departure",
            "arrival",
            "boarding",
            "boarding gate",
            "immigration",
            "customs",
            "transit",
            "layover"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "flight":{
        "keywords":{
            "flight",
            "airline",
            "ticket",
            "seat",
            "economy",
            "business class",
            "first class",
            "boarding pass",
            "check in luggage"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "documents":{
        "keywords":{
            "passport",
            "visa",
            "travel insurance",
            "international drivers license",
            "idrp",
            "idp"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "luggage":{
        "keywords":{
            "luggage",
            "baggage",
            "carry on",
            "checked baggage",
            "checked luggage",
            "backpack",
            "suitcase"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "transport":{
        "keywords":{
            "taxi",
            "grab",
            "uber",
            "train",
            "subway",
            "metro",
            "bus",
            "tram",
            "ferry",
            "cruise",
            "car rental",
            "road trip",
            "motorcycle rental"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

    "activities":{
        "keywords":{
            "museum",
            "temple",
            "beach",
            "mountain",
            "island",
            "camping",
            "hiking",
            "photography",
            "festival",
            "food tour",
            "night market",
            "walking tour"
        },
        "confidence":1.0,
        "last_updated":None,
        "source":"manual",
        "relationships":set(),
    },

}