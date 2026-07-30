"""
===========================================================
AIOS Photography Keyword Registry
core/keywords/registries/photography.py
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

PHOTOGRAPHY = {

    "camera": {

        "keywords": {

            "camera",
            "body",
            "dslr",
            "mirrorless",
            "canon",
            "nikon",
            "sony",
            "fujifilm",
            "lumix",

        },

        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),

    },

    "lens": {

        "keywords": {

            "lens",
            "prime",
            "zoom",
            "telephoto",
            "wide angle",
            "macro",
            "fisheye",

        },

        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),

    },

    "exposure": {

        "keywords": {

            "iso",
            "aperture",
            "shutter",
            "shutter speed",
            "exposure",
            "f stop",
            "brightness",

        },

        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),

    },

    "composition": {

        "keywords": {

            "composition",
            "rule of thirds",
            "leading lines",
            "framing",
            "symmetry",
            "foreground",
            "background",

        },

        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),

    },

    "editing": {

        "keywords": {

            "lightroom",
            "photoshop",
            "editing",
            "edit",
            "post processing",
            "post-processing",
            "raw",
            "jpeg",
            "jpg",
            "color grading",

        },

        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),

    },

}
