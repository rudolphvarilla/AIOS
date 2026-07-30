"""
AIOS Information Commands
core/commands/information.py

Commands that display information about AIOS.
"""

from core.commands.registry import COMMANDS

def help_command():

    print()

    print("============== HELP ==============")

    for category, commands in COMMANDS.items():

        print()

        print(category)

        print("-" * len(category))

        for command in commands:

            print(command)

    print()