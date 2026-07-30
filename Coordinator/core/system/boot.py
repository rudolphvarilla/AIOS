"""
AIOS Boot Manager
core/system/boot.py

Initializes every core AIOS subsystem.

Coordinator should never manually construct
individual managers or services.

Version 3
"""

from core.system.services import ServiceRegistry

from core.repository.manager import RepositoryManager
from core.scheduler.manager import Scheduler
from core.developer.manager import DeveloperMode
from core.models.manager import ModelManager
from core.tools.manager import ToolManager
from core.decision.engine import DecisionEngine
from core.time.manager import TimeManager


class AIOSBoot:

    def initialize(self):

        print("Initializing AIOS...")

        # ---------------------------------
        # Shared Managers
        # ---------------------------------

        time = TimeManager()

        services = ServiceRegistry(

            repository=RepositoryManager(time),

            scheduler=Scheduler(time),

            developer=DeveloperMode(),

            model_manager=ModelManager(),

            tool_manager=ToolManager(),

            decision_engine=DecisionEngine(),

            time=time

        )

        print("Initialization complete.")

        return services