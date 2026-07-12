# Presentation (Phase 12)

## Demo Script Outline

1. **Hook (30s):** the digital arrest / KYC scam scenario — describe the citizen's experience.
2. **Live demo (2–3 min):** submit the seeded SMS + transaction from `PROJECT_CONTEXT.md`'s demo scenario → show per-agent verdicts appearing → show the Fusion Agent's final verdict and recommended actions.
3. **Architecture (1 min):** show `docs/architecture.md`'s diagram, emphasize the standard agent contract as the "agentic" part — any agent can be added/removed without touching the others.
4. **What's built vs. roadmap (1 min):** be explicit. State which agents are real (MVP) and which stretch phases were completed. Do not imply Future-scope items (production deployment, full police portal, live dispatch) are built.
5. **Close:** impact framing — victims, banks, and police get a shared, explainable intelligence layer instead of siloed tools.

## Slide Checklist

- [ ] Title + problem statement
- [ ] Architecture diagram (`docs/architecture.md`)
- [ ] Agent contract / "why this is agentic, not just multiple models" slide
- [ ] Live demo (or recorded backup video — record one by Day 5)
- [ ] Tech stack + datasets used (from `docs/api.md`)
- [ ] What's built (MVP + completed stretch phases) vs. Future scope — from `MASTER_PLAN.md`
- [ ] Impact / who benefits (citizens, banks, telecom, police)
- [ ] Future scope slide (Phase 11 + unbuilt stretch phases, framed honestly as roadmap)

## Judge Q&A Prep

Anticipate:
- "How do you handle class imbalance in the fraud model?" → PR-AUC/recall, SMOTE/class-weighting (see `docs/api.md`).
- "Is the Fusion Agent actually reasoning, or just averaging scores?" → weighted aggregation + rules layer over standard-contract evidence; explain the escalation rule.
- "What happens if an agent fails or times out?" → Orchestrator should degrade gracefully (partial fusion over whichever agents responded) — confirm this is actually implemented before demo day.
- "What's real vs. future scope?" → answer directly from the What's Built slide; do not overclaim Phase 11 or unbuilt stretch phases.

## Recording a Backup Demo

Do this by Day 5 of the build (see `MASTER_PLAN.md` §Timeline) — live demos fail during actual presentations more often than teams expect. A 90-second screen recording of the working end-to-end flow is cheap insurance.
