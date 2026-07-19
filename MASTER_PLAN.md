# MASTER_PLAN.md — SentinelAI Complete Roadmap

This is the single source of truth for scope, phases, and sequencing. `PROJECT_CONTEXT.md` tracks *where we are* against this plan; this file defines *the whole plan*. Update this file only when scope itself changes — not on every sprint (that's what `CHANGELOG.md` and `TODO.md` are for).

Non-negotiable engineering rules live in `SYSTEM_RULES.md`; how to brief an AI coding assistant lives in `AI_GUIDELINES.md`; a ready-to-paste prompt for each phase below lives in `prompts/Sprint-NN.md`.

---

## Current Progress

- **Sprint 00 (Project Planning):** COMPLETED
- **Sprint 01 (Dataset Engineering):** COMPLETED
- **Sprint 02 (AI Agent Implementation):** COMPLETED
- **Sprint 03 (Intelligence Fusion & Orchestration):** COMPLETED
- **Sprint 04 (Citizen Portal MVP):** COMPLETED
- **Sprint 05 (Police Dashboard MVP):** COMPLETED
- **Sprint 06 (Production Readiness & Handoff):** COMPLETED

---

## 1. Scope: MVP / Stretch / Future

12 phases, each with its own dataset/training implication, is a multi-month product, not a hackathon build. Pick a track per phase and commit to it. A judge remembers one thing done well more than eight things done shallowly.

| Track | Phases | Rule |
|---|---|---|
| **MVP — build first, always demoable** | 0, 1 (partial), 3 (Fraud), 4 (Scam Comm.), 6 (Fusion), 9 (Orchestrator), 10 (minimal dashboard) | Must work end-to-end before anything else is touched |
| **Stretch — add only after MVP works end-to-end** | 2 (Currency), 5 (Voice), 7 (Graph), 8 (Geo) | Pick at most one or two, fully working, rather than several half-working |
| **Future scope — describe in slides, do not build** | 11 (production deployment), full police portal in 10, live dispatch/FIR/account-freeze automation, multi-tenant auth | Fine as roadmap slides only |

> An agent not wired into the Orchestrator by demo day is worse than not building it — it's a broken code path. Build depth-first (one full pipeline working) before breadth-first.

---

## 2. System Architecture (summary — full detail in `docs/architecture.md`)

```text
Citizen / Police / Bank / Telecom
                │
                ▼
        Orchestrator Agent (FastAPI, async fan-out)
                │
 ┌──────────────┼───────────────┬────────────────┐
 ▼              ▼                ▼                ▼
Scam Comm.   Fraud (txn)   Currency [stretch]  Voice [stretch]
 Agent         Agent          Agent               Agent
   │              │                │                │
   └──────────────┴────────┬───────┴────────────────┘
                            ▼
                Intelligence Fusion Agent
                            │
             ┌──────────────┴──────────────┐
             ▼                              ▼
     Graph Agent [stretch]           Geo Agent [stretch]
                            │
                            ▼
                 Alert & Report Agent
                            │
                            ▼
          Police Dashboard / Citizen App (React)
```

Every agent talks to the Orchestrator/Fusion Agent via one standard JSON contract — see `docs/api.md`. This is what makes it genuinely agentic rather than a pipeline: any agent can be mocked, swapped, or dropped without touching the others.

---

## 3. Phase-by-Phase Plan

### Phase 0 — Project Planning — `[MVP]`
**Objective:** Design the entire system before writing any code.
**AI does:** Architecture, folder structure, DB schema, tech stack, REST API design, agent definitions, communication contract.
**You do:** Git/GitHub repo, install VS Code/Python/Node.js/PostgreSQL. Install Neo4j *only* if attempting Phase 7 — otherwise use the NetworkX fallback (`docs/database.md`).
**Deliverables:** Folder structure, architecture doc, README, roadmap, DB schema, API docs.
**Done when:** Fully planned, agent contract and DB schema written, one demo scenario scripted on paper — no implementation yet.

### Phase 1 — Dataset Engineering — `[MVP, scoped down]`
**Objective:** Clean, standardized datasets — built per-agent, just before that agent's phase, not all five upfront.
**AI does:** Preprocessing scripts, missing-value handling, cleaning, label encoding, class balancing (SMOTE/class-weighting), feature engineering.
**You do:** Download the datasets listed in `docs/api.md` §Data Sources; place under `datasets/`; run and verify preprocessing.
**Done when:** MVP agent datasets (Fraud, Scam Comm.) are ready; stretch datasets only if that phase is reached.

### Phase 2 — Currency Agent — `[Stretch]`
**Objective:** Detect counterfeit Indian currency from an image.
**AI does:** CNN/YOLO model, training + inference pipeline, FastAPI service (standard contract), evaluation, Grad-CAM explainability.
**Data:** "Indian currency dataset" (Kaggle/Roboflow).
**Fallback:** rule-based watermark-region check + lightweight classifier instead of full YOLO if data quality/time is short.
**Done when:** Model evaluated on real images with reported precision/recall — attempt only after MVP is fully working end-to-end.

### Phase 3 — Fraud Agent — `[MVP]`
**Objective:** Detect fraudulent financial transactions.
**AI does:** XGBoost/Random Forest/LightGBM, SHAP explainability, REST API (standard contract).
**Data:** Kaggle "Credit Card Fraud Detection" (ULB) or "IEEE-CIS Fraud Detection" — both imbalanced; report PR-AUC/recall, not accuracy.
**Done when:** Best model selected and deployed locally behind `/analyze`.

### Phase 4 — Scam Communication Agent — `[MVP]`
**Objective:** Detect scam SMS + phishing URLs (email is optional/stretch).
**AI does:** Text classifier (BERT/IndicBERT if time allows; TF-IDF + XGBoost is a legitimate fallback); feature-based XGBoost for URLs.
**Data:** Kaggle "SMS Spam Collection" + UCI SMS Spam, **plus 100–200 hand-labeled India-specific scam messages** (digital arrest, fake KYC, lottery — the hand-labeled set matters more than volume); Kaggle "Phishing Website Dataset" (UCI) or PhishTank export for URLs.
**Done when:** Returns verdict + category + risk score + explanation on the standard contract — must be real, not mocked, by end of MVP window.

### Phase 5 — Voice Intelligence Agent — `[Stretch — highest risk, attempt last]`
**Objective:** Analyze voice recordings for spoofing, emotion, impersonation.
**AI does:** STT, spoof detection, emotion detection, impersonation detection, threat scoring.
**Data:** Common Voice (STT baseline), ASVspoof (spoof detection).
**Critical fallback:** do not train any of these three sub-models from scratch — use pretrained Whisper-small (`faster-whisper`) + a pretrained ASVspoof checkpoint; cut emotion detection first if time is tight.
**Done when:** Attempted only after Currency/Graph/Geo are ruled out or complete; scope to STT + spoof detection only.

### Phase 6 — Intelligence Fusion Agent — `[MVP]`
**Objective:** Central reasoning engine — consumes standard-contract outputs from all active agents for a `case_id`, does not analyze raw data itself.
**Logic:** weighted aggregation + a small rules layer (e.g. "if 2+ agents report fraud with risk_score > 80, escalate to organized-scam verdict") is a legitimate reasoning engine for the demo — doesn't require its own ML model.
**Done when:** Produces a final verdict, overall risk score, narrative, and recommended actions. **Do not let this slip past Day 3 of the build** — it's the phase judges care about most.

### Phase 7 — Graph Intelligence Agent — `[Stretch]`
**Objective:** Identify fraud rings, mule accounts, shared devices, repeat offenders across victims/phones/devices/accounts/merchants.
**AI does:** Neo4j graph model or NetworkX equivalent (`docs/database.md`).
**Fallback:** NetworkX in-memory graph + `pyvis`/`matplotlib` visualization if Neo4j setup eats time — have this ready before you need it.
**Done when:** attempted only if MVP + at most one other stretch phase are already solid.

### Phase 8 — Geospatial Intelligence Agent — `[Stretch]`
**Objective:** Crime heatmaps, district risk analysis, patrol recommendations, fraud density maps.
**Tech:** Leaflet + OpenStreetMap.
**Done when:** usually the fastest stretch phase to look visually impressive with seeded location data — good default if only one stretch phase is attempted.

### Phase 9 — Orchestrator Agent — `[MVP]`
**Objective:** Coordinate all active agents — no AI inference itself.
**Flow:** evidence in → fan out to active agents in parallel (`asyncio.gather`) → call Fusion Agent → call Alert Agent → return final report.
**Done when:** adding/removing a stretch agent is a config change, not a rewrite, because every agent honors the standard contract.

### Phase 10 — Dashboard — `[MVP: minimal version; full version is Stretch/Future]`
**MVP:** one flow — submit input → per-agent verdicts → fused verdict → recommended action. This alone is a complete, demoable product.
**Stretch (Citizen Portal):** scan currency, verify SMS/URLs, upload voice, report fraud.
**Future (Police Portal):** live alerts, analytics, heatmaps, network viz, investigation reports — build only with days to spare.

### Phase 11 — Deployment — `[Future scope — do not build]`
**Would include:** Dockerfiles, Compose, Nginx, Redis, Celery, GitHub Actions, cloud config.
**Reality:** a local `docker-compose.yml` (DB + built agents) is enough for the demo; everything else is a slide in `docs/deployment.md`, not a build task. This phase is the most common way hackathon teams run out of time — resist it.

### Phase 12 — Final Polish — `[MVP — always do this]`
**AI does:** Slides, architecture/flow/sequence diagrams, README, demo script, judge Q&A prep, and an honest future-scope slide covering whatever from Phases 2/5/7/8/11 wasn't built.
**Done when:** what's built vs. roadmap is clearly distinguished — judges respond better to honest scoping than overclaiming.

---

## 4. Timeline (6-day build)

| Day | Focus | Deliverable |
|---|---|---|
| 0 | Phase 0 | Repo, agent contract, DB schema applied, demo scenario scripted |
| 1 | Phase 9 + Phase 4 stubbed | `/analyze` mocked, wired through Orchestrator to a placeholder dashboard |
| 2 | Phase 4 + Phase 3 real models | Scam Comm. and Fraud return real predictions |
| 3 | Phase 6 + Phase 10 (minimal) | End-to-end demo works. **Demo-safe from this point.** |
| 4 | ONE stretch phase (2, 5, 7, or 8) | Fully working, not several half-working |
| 5 | Alert/Report agent, dashboard polish, error handling, seeded demo data | Stable under a live demo |
| 6 | Phase 12 | Presentation-ready |

If behind at end of Day 3: skip all stretch phases, harden the MVP instead. A rock-solid 3-agent demo beats a fragile 6-agent one.

---

## 5. Biggest Risks

1. **Voice Agent (Phase 5)** bundles three hard sub-problems — attempt last, STT + spoof only.
2. **Fraud/scam datasets are imbalanced** — report precision/recall/PR-AUC, not accuracy.
3. **Explainability (Grad-CAM, SHAP) is real extra work** — budget time explicitly.
4. **Neo4j is heavy infra for a demo** — NetworkX fallback ready in advance.
5. **Phase 11 is a common time sink** — local `docker-compose.yml` is enough; rest is a slide.
