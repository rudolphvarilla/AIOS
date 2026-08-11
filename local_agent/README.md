# AIOS Local Agent

Phase 3.2.1v2 foundation for controlled remote development and test execution on the Windows AIOS workstation.

## Purpose

The local agent is a controlled bridge between a remote development controller and the local AIOS workspace. It is deliberately separated from `coordinator.py` so Coordinator remains a coordinator.

Initial responsibilities:

- verify the AIOS workspace and virtual environment
- run the canonical regression suite
- run an AIOS query through the existing developer workflow
- capture stdout, stderr, exit code, and timing
- provide structured results suitable for a future authenticated remote relay

## Current security boundary

This first implementation is local-only. It must **not** be exposed directly to the public internet. Remote transport/authentication will be added as a separate, explicitly reviewed Stem.

## Planned progression

1. Local command execution and structured result capture.
2. Verify the existing `developer_shell.bat` workflow.
3. Add authenticated outbound remote transport without exposing a raw shell.
4. Add crash/reproduction bundle capture.
5. Add Git/test orchestration.
6. Integrate with the post-stabilization Mobile workstation capability.
