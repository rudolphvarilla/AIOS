"""
===========================================================
AIOS Search Entity Classifier
core/search/classifier.py
===========================================================

Assigns semantic types to extracted entities.

Version 1.0
===========================================================
"""

import re
from core.keywords.lexicon.entities import ENTITY_KEYWORDS

class SearchEntityClassifier:

    def classify(self, entities):

        for entity in entities:

            entity.entity_type = self.detect(entity.name)

        return entities

    # -------------------------------------------------

    def detect(self, name):

        text = name.casefold()

        # -----------------------------------------
        # Exact AIOS Entity Lexicon
        # -----------------------------------------

        entity_type = ENTITY_KEYWORDS.get(text)

        if entity_type:
            return entity_type

        # -----------------------------
        # Website
        # -----------------------------

        if any(

            domain in text

            for domain in (

                ".com",
                ".org",
                ".net",
                ".gov",
                ".edu",

            )

        ):

            return "WEBSITE"

        # -----------------------------
        # Airport
        # -----------------------------

        if "airport" in text:

            return "AIRPORT"

        # -----------------------------
        # Hotel
        # -----------------------------

        HOTEL_WORDS = (

            "hotel",
            "inn",
            "resort",
            "hostel",
            "hyatt",
            "hilton",
            "aman",
            "marriott",
            "westin",
            "sheraton",

        )

        if any(word in text for word in HOTEL_WORDS):

            return "HOTEL"

        # -----------------------------
        # Camera
        # -----------------------------

        CAMERA_BRANDS = (

            "canon",
            "nikon",
            "sony",
            "fujifilm",
            "lumix",
            "leica",

        )

        if any(word in text for word in CAMERA_BRANDS):

            return "CAMERA"

        # -----------------------------
        # NAS
        # -----------------------------

        NAS_BRANDS = (

            "ugreen",
            "synology",
            "qnap",
            "terramaster",

        )

        if any(word in text for word in NAS_BRANDS):

            return "NAS"

        return "UNKNOWN"