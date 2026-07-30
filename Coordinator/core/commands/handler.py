"""
AIOS Command Handler

Routes built-in AIOS commands.
"""

from core.commands.system import (status_command, clear_command)
from core.commands.version import version_command
from core.commands.version import about_command
from core.commands.scheduler import (jobs_command, run_jobs_command, results_command)
from core.commands.information import help_command

def handle_command(command, memory, state, developer, scheduler):

    command = command.lower()

    if command == "/help":

        help_command()

        return "CONTINUE"

    elif command == "/status":

        status_command(memory, state, developer)

        return "CONTINUE"

    elif command == "/time":

        print()
        print("================ TIME ================")
        print()
        print(f"Now        : {state.time.now()}")
        print(f"Date       : {state.time.date()}")
        print(f"Time       : {state.time.time()}")
        print(f"Weekday    : {state.time.weekday()}")
        print(f"Timestamp  : {state.time.timestamp()}")
        print()

        return "CONTINUE"

    elif command == "/version":

        version_command()

        return "CONTINUE"

    elif command == "/about":

        about_command()

        return "CONTINUE"

    elif command == "/dev on":

        developer.enable()

        return "CONTINUE"

    elif command == "/dev off":

        developer.disable()

        return "CONTINUE"

    elif command == "/dev sim on":

        developer.simulation = True

        print()

        print("Developer Simulation ENABLED.")

        return "CONTINUE"

    elif command == "/dev sim off":

        developer.simulation = False

        print()

        print("Developer Simulation DISABLED.")

        return "CONTINUE"

    elif command == "/jobs":

        jobs_command(scheduler)

        return "CONTINUE"

    elif command == "/run jobs":

        run_jobs_command(scheduler)

        return "CONTINUE"

    elif command == "/results":

        results_command(scheduler)

        return "CONTINUE"

    elif command == "/clear":

        clear_command(memory)

        return "CONTINUE"

    elif command == "/exit":

        return "EXIT"

    #KEEP BELOW AT END OF THIS FUNCTION. If no "/"commands are available, system will default to use this.
    elif command.startswith("/"):

        print()

        print(f"Unknown command: {command}")

        print()

        print("Type /help to see available commands.")

        return "CONTINUE"


    return None