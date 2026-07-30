\# AIOS Coordinator Changelog



All notable changes to the AIOS Coordinator are documented here.



This project follows an incremental development model where each version represents a completed architectural milestone.



\---



\## 0.9.5



Added



\- Boot Manager

\- Decision Engine

\- Prompt Inspector

\- Search Injection



Changed



\- Prompt Builder now injects memory



Fixed



\- Prompt ordering bug

\- Search injection timing



\# v0.8.1 (Current Development Build)



\### Maintenance



\- Migrated DuckDuckGo provider from duckduckgo\_search to the maintained ddgs package.

\- Removed deprecated search package warning.

\- Verified full Search Service → Provider → Internet pipeline.

\- First successful live Internet search completed.



\---



\# v0.8



\### Service \& Search Architecture



Added:



\- Service Registry

\- Service Manager

\- Search Service

\- Provider Registry

\- Provider Manager

\- DuckDuckGo Provider

\- Search Results stored in AIOS State



Architecture:



User

→ Intent Classification

→ Complexity Classification

→ Planner

→ Capability Router

→ Executor

→ Service Manager

→ Search Service

→ Provider Manager

→ DuckDuckGo

→ Internet



Completed:



\- First complete AIOS Service architecture

\- First Provider architecture

\- First live external data retrieval



\---



\# v0.7



\### Tool Architecture



Added:



\- Tool Registry

\- Tool Manager

\- Capability-based Tool Selection



Completed:



\- Executor delegates external work through Tool Manager.



\---



\# v0.6



\### Model Routing



Added:



\- Model Registry

\- Model Manager

\- Capability Routing

\- Complexity-based Model Selection



Completed:



\- Automatic model selection

\- Exact vs closest-complexity fallback



Supported Models:



\- qwen3:4b

\- qwen3:8b

\- qwen2.5-coder:3b



\---



\# v0.5



\### Memory Foundation



Added:



\- Working Memory

\- Session Memory

\- Recall Engine

\- Background Queue

\- Performance Monitor



Completed:



\- Context persistence between requests.

\- Background task queue.



\---



\# v0.4



\### Execution Planning



Added:



\- Execution Planner

\- ExecutionPlan dataclass



Completed:



\- Intent → Execution Plan pipeline.



\---



\# v0.3



\### Intent Classification



Added:



\- Intent detection

\- Complexity classification



Supported Intents:



\- GENERAL

\- CODING

\- DOCUMENT



\---



\# v0.2



\### Core Coordinator



Added:



\- Coordinator loop

\- Developer simulation mode

\- Benchmark foundation



\---



\# v0.1



\### Project Initialization



Created:



\- AIOS Coordinator project

\- Folder architecture

\- Initial module structure



\---

