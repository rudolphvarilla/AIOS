"""
===========================================================
AIOS Weather Keyword Registry
core/keywords/registries/weather.py
===========================================================

Semantic candidates for weather and outdoor conditions.

This registry is NOT a fact ontology. It only helps route ambiguous language
and identify weather-related context. Actual facts are extracted from source
evidence at runtime.

Version 1.0
===========================================================
"""

WEATHER = {
    "weather": {
        "keywords": {
            "weather", "forecast", "forecasts", "conditions",
            "meteorology", "climate", "weather report",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "precipitation": {
        "keywords": {
            "precipitation", "rain", "rainfall", "rain chance",
            "chance of rain", "snow", "snowfall", "new snow",
            "fresh snow", "powder", "powder snow", "sleet", "hail",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "atmospheric_conditions": {
        "keywords": {
            "humidity", "wind", "wind speed", "gust", "pressure",
            "air pressure", "low pressure area", "high pressure area",
            "monsoon", "storm", "typhoon", "tropical depression",
            "thunderstorm", "lightning", "visibility", "cloud cover",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "winter_outdoor": {
        "keywords": {
            "snow depth", "freezing level", "snow line", "powder day",
            "ski conditions", "snow conditions", "snowboard conditions",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
}
