"""
AIOS Routing Table
core/routing/routes.py

Defines execution routes for every detected intent.

The Capability Router simply loads these routes.

Version 2

Execution Routes now include Prompt Planning.

Execution Flags
---------------
browser
vision
image_generation

Prompt Flags
------------
repository
memory
profile
workspace
time
longterm
"""

ROUTES = {

    "GENERAL": {

        # Model Routing

        "model_capability": "GENERAL",

        "tool_capability": None,

        # Prompt Planning

        "repository": False,

        "memory": False,

        "profile": False,

        "workspace": False,

        "time": False,

        "longterm": False,

        # Execution

        "browser": False,

        "vision": False,

        "image_generation": False,

    },

    "CODING": {

        "model_capability": "CODING",

        "tool_capability": None,

        "repository": False,

        "memory": False,

        "profile": False,

        "workspace": False,

        "time": False,

        "longterm": False,

        "browser": False,

        "vision": False,

        "image_generation": False,

    },

    "DOCUMENT": {

        "model_capability": "GENERAL",

        "tool_capability": "DOCUMENT_QA",

        "repository": False,

        "memory": True,

        "profile": False,

        "workspace": False,

        "time": False,

        "longterm": False,

        "browser": False,

        "vision": False,

        "image_generation": False,

    },

}

DEFAULT_ROUTE = {

    "model_capability": "GENERAL",

    "tool_capability": None,

    "repository": False,

    "memory": False,

    "profile": False,

    "workspace": False,

    "time": False,

    "longterm": False,

    "browser": False,

    "vision": False,

    "image_generation": False,

}