# AIOS Local Agent

Phase 3.2.1v2 foundation for controlled remote development and test execution on the Windows AIOS workstation.

## Purpose

The local agent is a controlled bridge between a remote development controller and the local AIOS workspace. It is deliberately separated from `coordinator.py` so Coordinator remains a coordinator.

Initial responsibilities:

- verify the AIOS workspace and virtual environment
- run the three standard real-AIOS regression queries through Coordinator
- run an AIOS query through the existing developer workflow
- capture stdout, stderr, exit code, and timing
- provide structured results suitable for a future authenticated remote relay

## Commands

```bat
local_agent\run_agent.bat verify
local_agent\run_agent.bat git-status
local_agent\run_agent.bat query "what is 2+2"
local_agent\run_agent.bat regression
```

`regression` runs these queries in order, with a 300-second timeout for each:

- R1: `current weather in philippines`
- R2: `tallest mountain in the philippines`
- R3: `what is 2+2`

It prints one JSON report containing the status, success flag, return code,
captured stdout/stderr, error (including `timeout`), and elapsed time for every
case. Use `--timeout SECONDS` to set a different per-query limit.

## Current security boundary

This first implementation is local-only. It must **not** be exposed directly to the public internet. Remote transport/authentication will be added as a separate, explicitly reviewed Stem.

## Planned progression

1. Local command execution and structured result capture.
2. Verify the existing `developer_shell.bat` workflow.
3. Add authenticated outbound remote transport without exposing a raw shell.
4. Add crash/reproduction bundle capture.
5. Add Git/test orchestration.
6. Integrate with the post-stabilization Mobile workstation capability.
