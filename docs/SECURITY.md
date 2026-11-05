# Security model and production gaps

## Included
- Specialist-specific allowlists.
- Runtime tool authorization independent of natural-language instructions.
- Fictional fixture data.
- `.env` and local memory file excluded from Git.

## Not included
- User authentication or account ownership verification.
- PII detection/redaction, encryption at rest, tenant isolation, or retention automation.
- API rate limits, secrets manager, immutable audit storage, or cloud IAM.
- Production-grade policy engine or formal security review.

Never connect this demo to real customer systems or store sensitive customer conversations without implementing and reviewing these controls.
