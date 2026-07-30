\# AIOS Architecture



\## Current Version



0.9.5-alpha.1



\---



\# Project Goal



Artificial Intelligence Operating System



Purpose:

Coordinate multiple AI models, memory systems,

services, providers and autonomous agents.



\---



\# Current Stage



Core Infrastructure Stabilization



Completed



\- Coordinator

\- Boot Manager

\- Decision Engine

\- Prompt Builder

\- Memory Manager

\- Search Service

\- Provider Manager

\- Tool Manager

\- Version Manager



\---



\# Boot Sequence



AIOSBoot



↓



Memory Manager



↓



Scheduler



↓



Developer Mode



↓



Model Manager



↓



Tool Manager



↓



Decision Engine



↓



Coordinator Ready



\---



\# Execution Flow



User Input



↓



Intent Classifier



↓



Planner



↓



Decision Engine



↓



Model Manager



↓



Tool Manager



↓



Executor



↓



Prompt Builder



↓



LLM



↓



Repository



↓



Output



\---



\# Current Models



qwen3:4b

Role:

Fast reasoning



qwen3:8b

Role:

Deep reasoning



qwen2.5-coder

Role:

Programming



\---



\# Services



DuckDuckGo Search



Recall Engine



Session Memory



Working Memory



\---



\# Future Modules



Information Repository



Knowledge Graph



Qdrant



Graphify



Workspace Manager



AIOS.md



Obsidian



Background Watchers



Translation Engine



Autonomous Scheduler



Notification System



UI



Mobile Client



NAS Integration



\---



\# Design Philosophy



AIOS never depends directly on a storage engine.



Coordinator only communicates with interfaces.



All implementations are replaceable.



\---



\# Current Roadmap



v0.9



Infrastructure



v1.0



Information Repository



Background Workers



Workspace Context



v2.0



Knowledge Graph



Long-Term Memory



UI



Autonomous AI

