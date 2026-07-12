# Sprint Prompt Template

Every Sprint-NN.md follows this shape. Copy it when adding a new sprint prompt (e.g. if a phase gets split in two).

```
Paste PROJECT_CONTEXT.md here first.

Then:

We are working on Phase <N> — <name> ([MVP|Stretch|Future]) of SentinelAI.

Objective: <from MASTER_PLAN.md>

Scope for this sprint (do NOT exceed):
<the phase's "AI does" / "Data" / "Fallback" bullets from MASTER_PLAN.md>

Constraints:
- Follow SYSTEM_RULES.md and AI_GUIDELINES.md exactly.
- Every agent endpoint must match the Agent Contract in docs/api.md.
- No hardcoded config — read from configs/*.yaml.
- Include a smoke test in tests/ for any new endpoint.
- Do not build anything tagged Future scope in MASTER_PLAN.md.

Deliverables expected this sprint:
<from MASTER_PLAN.md's phase section>

Done when:
<the phase's "Done when" line from MASTER_PLAN.md>

At the end, list what should change in PROJECT_CONTEXT.md, CHANGELOG.md, and TODO.md.
```
