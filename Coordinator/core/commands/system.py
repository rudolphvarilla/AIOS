"""
AIOS System Commands

Implements built-in AIOS commands.

system command code for:
-status_command
-clear_command
"""

def status_command(memory, state, developer):

    print("\n========== AIOS STATUS ==========\n")

    if state.plan:

        print(f"Intent           : {state.intent}")
        print(f"Complexity       : {state.plan.complexity}")
        print(f"Capability       : {state.plan.capability}")

    print()

    print(f"Current Model    : {state.selected_model}")
    print(f"Current Tool     : {state.selected_tool}")

    print()

    print("Working Memory   : Active")
    print(f"Session Entries  : {len(memory.session.history)}")

    print(f"Developer Mode     : {'ON' if developer.enabled else 'OFF'}")
    print(f"Simulation         : {'ON' if developer.simulation else 'OFF'}")
    print()

    print("\n=================================\n")


def clear_command(memory):

    memory.working.reset()

    memory.session.history.clear()

    print("\nConversation cleared.\n")