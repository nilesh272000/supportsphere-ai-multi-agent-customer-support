# SupportSphere AI — Multi-Agent Customer Support System

A portfolio-ready, modular customer-support orchestration demo. A coordinator classifies requests, delegates to focused specialists, enforces tool permissions in code, and returns a concise customer-facing response. Includes local conversation memory, fixture-backed tools, evaluation cases, and unit tests.

## Architecture

```text
Customer
   |
   v
Coordinator / Router
   |---- Billing Specialist ---- invoice lookup (billing-only)
   |---- Shipping Specialist --- order status (shipping-only)
   |---- Refund Specialist ----- refund policy lookup
   |
   +---- Conversation Memory (local JSON)
   |
   v
Response Composer -> Customer
```

## Highlights
- Explicit coordinator-to-specialist orchestration.
- Least-privilege tool registry: each specialist receives only approved tools.
- Runtime authorization checks reject disallowed tool calls.
- Fixture-backed invoice, order, and refund-policy tools.
- Lightweight persistent conversation history (local JSON file).
- Deterministic routing and response composition for easy local testing.
- Evaluation dataset and basic routing/response checks.
- No external API key required for the demo.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e .
supportsphere ask "Where is my order ORD-8871?"
supportsphere ask "Can you check invoice INV-1042?"
supportsphere eval
```

Or run without installing:
```bash
python -m supportsphere.cli ask "How long does a refund take?"
python -m supportsphere.cli eval
```

## Example prompts
- `Where is my order ORD-8871?`
- `Can you check invoice INV-1042?`
- `How long does a refund take?`
- `I need help with a payment on invoice INV-2048.`

## Project structure
```text
SupportSphere-AI-Multi-Agent-Customer-Support/
├── src/supportsphere/
│   ├── __init__.py
│   ├── agents.py          # coordinator and specialist workflows
│   ├── memory.py          # local conversation history
│   ├── policy.py          # tool authorization boundary
│   ├── tools.py           # fixture-backed business tools
│   └── cli.py             # command-line interface
├── tests/
│   ├── test_agents.py
│   └── test_policy.py
├── eval/
│   └── cases.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── SECURITY.md
├── pyproject.toml
└── README.md
```

## Design notes
This implementation intentionally uses deterministic Python orchestration rather than a hosted LLM agent framework. That keeps the workflow inspectable and testable without credentials. The coordinator and specialists are agent-like components, not autonomous LLMs. Replace the fixture tools with authenticated CRM, billing, and fulfilment APIs before production use.

## Security boundaries and limitations
- Tool access is enforced by Python policy checks and specialist-specific allowlists; prompts are not used as the security boundary.
- Sample customer/order/invoice data is fictional.
- Local JSON memory is for demonstration only; it is not encrypted, multi-tenant, or suitable for sensitive customer data.
- No Google ADK, Gemini API, Vertex AI deployment, A2A endpoint, cloud IAM integration, or production observability is included.
- The demo does not guarantee identity verification, PCI compliance, or regulatory compliance.
- Tool authorization is not a substitute for authentication, authorization infrastructure, audit retention, or secure secret management.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Suggested extensions
1. Add authenticated CRM and order-management adapters.
2. Add a real LLM provider behind a narrow model interface.
3. Add persistent database-backed memory with tenant isolation and retention controls.
4. Add human escalation and redaction workflows.
5. Add offline and LLM-as-judge evaluation with curated golden cases.

## License
MIT. See `LICENSE`.
