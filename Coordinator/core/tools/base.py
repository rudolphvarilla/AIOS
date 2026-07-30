"""
AIOS Tool Definition

Defines the structure of every external tool
known by AIOS.

The Tool Manager uses this definition when
registering available tools.

Version 1:
- Tool metadata only
- No execution logic
"""

from dataclasses import dataclass

@dataclass
class ToolConfig:

    name: str

    capability: str

    available: bool

    description: str