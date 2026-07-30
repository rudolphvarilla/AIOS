"""
AIOS Version Information

Displays version and project information.

All version metadata comes from
core.system.version.
"""

from core.system.version import *


def version_command():

    print("\n========== AIOS VERSION ==========\n")

    print(f"AIOS               : {FULL_VERSION}")
    print(f"Project            : {PROJECT}")
    print(f"Python             : {PYTHON_VERSION}")
    print(f"Build Date         : {BUILD_DATE}")
    print(f"Author             : {AUTHOR}")

    print()


def about_command():

    print("\n========== ABOUT AIOS ==========\n")

    print(PROJECT)
    print()

    print(f"Version : {FULL_VERSION}")
    print(f"Author  : {AUTHOR}")
    print(f"Python  : {PYTHON_VERSION}")

    print()

    print("Current Stage")
    print("-------------")
    print("Core Infrastructure Stabilization")

    print()

    print("Core Components")
    print("----------------")
    print("✓ Coordinator")
    print("✓ Boot Manager")
    print("✓ Decision Engine")
    print("✓ Prompt Builder")
    print("✓ Memory System")
    print("✓ Search Service")
    print("✓ Provider Manager")
    print("✓ Model Manager")
    print("✓ Tool Manager")

    print()