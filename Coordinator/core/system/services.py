"""
AIOS Service Registry

Single container for every runtime service.

All core components are registered here during boot.

Future services:
- Localization
- Time
- Notification
- Browser
- Vision
- Watchers
- Qdrant
- Graphify
"""

from dataclasses import dataclass

from core.repository.manager import RepositoryManager
from core.scheduler.manager import Scheduler
from core.developer.manager import DeveloperMode
from core.models.manager import ModelManager
from core.tools.manager import ToolManager
from core.decision.engine import DecisionEngine


@dataclass
class ServiceRegistry:

    repository: RepositoryManager

    scheduler: Scheduler

    developer: DeveloperMode

    model_manager: ModelManager

    tool_manager: ToolManager

    decision_engine: DecisionEngine

    #
    # Reserved
    #

    time: object | None = None

    localization: object | None = None

    notification: object | None = None

    browser: object | None = None

    vision: object | None = None

    translation: object | None = None

    weather: object | None = None

    flights: object | None = None

    stocks: object | None = None

    graph: object | None = None

    qdrant: object | None = None