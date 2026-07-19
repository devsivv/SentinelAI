# AI_GUIDELINES.md

Give this file to any AI coding assistant (ChatGPT, Claude, Claude Code, Cursor, etc.) at the start of a session, alongside `PROJECT_CONTEXT.md`. It exists so you don't re-explain engineering standards every session — `SYSTEM_RULES.md` defines *what* the rules are; this file defines *how the AI should behave* while applying them.

---

## Session Start Checklist (for the AI)

Before writing any code, read in this order:
1. `PROJECT_CONTEXT.md` — where the project is right now
2. The relevant phase entry in `MASTER_PLAN.md` — what this sprint's objective actually is, and its track (MVP/Stretch/Future)
3. `SYSTEM_RULES.md` — non-negotiable engineering rules
4. `docs/architecture.md` and `docs/api.md` — the agent contract, which every new agent must honor
5. The matching `prompts/Sprint-NN.md` file, if one exists, for this phase's specific scope

If any of these conflict with what the user is asking for in the moment, surface the conflict rather than silently picking one — e.g. "this would break the Agent Contract in SYSTEM_RULES.md, want me to proceed anyway or adjust the approach?"

## Coding Standards

- **Python:** 3.12, type-hinted, Pydantic models for all API I/O, `black`-formatted.
- **Naming:** `snake_case` for Python files/functions, `PascalCase` for Pydantic models and classes, agent folders named `<domain>_agent` (e.g. `fraud_agent`, `scam_comm_agent`).
- **Folder placement:** new agent → `agents/<name>_agent/`; new orchestrator/fusion logic → `backend/`; new UI → `frontend/`; new one-off utility → `scripts/`, not scattered in the repo root.
- **No hardcoding:** paths, ports, model paths, and dataset paths come from `configs/*.yaml`, never inline (`SYSTEM_RULES.md` §4).
- **No duplicate logic:** verdict/scoring logic exists in exactly one place per agent (`SYSTEM_RULES.md` §2). Before writing a new function, check whether equivalent logic already exists elsewhere in the repo.

## API Contracts & Integration

- Every agent implements `POST /analyze` and returns the exact schema in `docs/api.md` — do not invent new top-level response fields; agent-specific data goes inside `evidence`.
- When asked to build a new agent, generate the FastAPI app, the Pydantic request/response models (matching the shared contract), a `model.py` with the actual inference logic, and a smoke test in `tests/` — not just the happy-path endpoint.
- **Frontend Integration:** Never invent backend endpoints to satisfy frontend requirements. If backend capabilities intentionally do not exist (e.g., missing CRUD APIs for cases), use graceful mock fallbacks and preserve existing API contracts.
- **UI Architecture:** Prefer reusing existing React components, Layouts, and design systems. Do not redesign interfaces unless explicitly instructed.

## Documentation Requirements

Every AI-generated feature should come with:
- A docstring or short comment explaining *why*, not just *what*, for any non-obvious logic (e.g. why a particular imbalance-handling technique was chosen)
- An update to the relevant `docs/*.md` file if it changes an API shape, schema, or architectural decision
- No invented citations, benchmark numbers, or dataset statistics — if a metric isn't actually computed in this session, say so rather than fabricating a plausible-looking number

## Testing Expectations

- Hackathon-appropriate, not enterprise-appropriate: a smoke test per endpoint (`tests/test_<agent>.py`) verifying it returns contract-shaped JSON on one realistic input and handles one bad-input case gracefully.
- Do not skip tests "to save time" on MVP-track agents (Fraud, Scam Comm., Fusion, Orchestrator) — these are the ones that must not break on demo day.
- Stretch-track agents can ship with lighter testing if time is short, per `MASTER_PLAN.md`'s scope priorities.

## Scope Discipline (most important rule)

- Always check a request against the current phase's **track** in `MASTER_PLAN.md` before building. If asked to build something tagged Future scope, say so plainly and suggest it become a `docs/presentation.md` slide instead of code.
- Prefer using or fine-tuning a pretrained model over training one from scratch, per `docs/api.md`'s data-source notes — this is the single biggest timeline risk in the whole project, and an AI assistant defaulting to "let's train a custom model" is how it gets triggered.
- When a request is ambiguous about scope, default to the smallest version that satisfies the current phase's "Done when" criterion in `MASTER_PLAN.md`, and note what was deferred.

## End of Session

Remind the user (or self-update, if operating with file write access) to:
- Update `PROJECT_CONTEXT.md`
- Add a `CHANGELOG.md` entry
- Refresh `TODO.md` for the next sprint

This mirrors `SYSTEM_RULES.md` §5 — it's listed here too because it's the step most likely to get skipped under AI-assisted speed.
