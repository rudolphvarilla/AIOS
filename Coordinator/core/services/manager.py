"""
AIOS Service Manager

Central manager for all AIOS Services.

The Executor never communicates directly
with Providers.

Instead, it requests a Service, which
internally manages one or more Providers.

Version 1
- Static registry
- Capability selection
"""

from core.services.registry import SERVICES


class ServiceManager:

    def __init__(self):

        self.services = SERVICES

    # ----------------------------------
    # Register Service
    # ----------------------------------

    def register(self, name, config):

        self.services[name] = config

    # ----------------------------------
    # Get Service
    # ----------------------------------

    def get(self, name):

        return self.services.get(name)

    # ----------------------------------
    # Check if Service exists
    # ----------------------------------

    def exists(self, name):

        return name in self.services

    # ----------------------------------
    # List Services
    # ----------------------------------

    def list_services(self):

        return list(self.services.keys())

    # ----------------------------------
    # Select Service
    # ----------------------------------

    def select(self, capability):

        print("\nSelecting service...")
        print(f"Requested Capability : {capability}")

        for service in self.services.values():

            print(
                f"Checking -> {service.name} | "
                f"{service.capability}"
            )

            if (
                service.available
                and service.capability == capability
            ):

                print(f"Selected -> {service.name}")

                return service.instance

        print("No matching service found")

        return None