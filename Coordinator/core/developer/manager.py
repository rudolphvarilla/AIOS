"""
AIOS Developer Mode

Controls developer features.
"""

class DeveloperMode:

    def __init__(self):

        self.enabled = False
        self.simulation = False

    def enable(self):

        self.enabled = True

        print("\nDeveloper Mode ENABLED.\n")

    def disable(self):

        self.enabled = False

        print("\nDeveloper Mode DISABLED.\n")

    def toggle(self):

        self.enabled = not self.enabled

        if self.enabled:

            print("\nDeveloper Mode ENABLED.\n")

        else:

            print("\nDeveloper Mode DISABLED.\n")