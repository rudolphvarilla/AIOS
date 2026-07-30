"""
===========================================================
AIOS Command Registry
core/commands/registry.py
===========================================================

Single source of truth for every built-in AIOS command.

The Help command should NEVER hardcode commands.

Future

• Plugins
• Tool Commands
• Developer Extensions
===========================================================
"""

COMMANDS = {

    "SYSTEM": [

        "/help",
        "/status",
        "/clear",
        "/version",
        "/about",
        "/time",
        "/exit",

    ],

    "DEVELOPER": [

        "/dev on",
        "/dev off",
        "/dev sim on",
        "/dev sim off",

    ],

    "SCHEDULER": [

        "/jobs",
        "/run jobs",
        "/results",

    ],

}