# Architecture

## Request lifecycle
1. The coordinator receives a customer message and selects a specialist using transparent routing rules.
2. The specialist invokes a registered business tool through `ToolRegistry.call`.
3. The registry checks the specialist's allowlist before executing the handler.
4. The coordinator composes a customer-facing answer from the structured tool result.
5. The user/assistant turn is appended to a local session memory file.

## Why deterministic orchestration?
The project demonstrates agent boundaries, routing, tool contracts, least-privilege access, and memory without requiring an LLM key. A production extension can replace routing and response composition with an LLM while retaining authorization in ordinary code.
