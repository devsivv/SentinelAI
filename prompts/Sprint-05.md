# Sprint 05 — Voice Intelligence Agent `[Stretch — highest risk, attempt last]`

Paste `PROJECT_CONTEXT.md` here first.

**Only start this sprint after Currency/Graph/Geo have been ruled out or completed — confirm in `PROJECT_CONTEXT.md`.**

We are working on **Phase 5 — Voice Intelligence Agent (Stretch)** of SentinelAI.

**Objective:** Analyze voice recordings for spoofing and impersonation. Scope to STT + spoof detection only — cut emotion detection first if time is tight.

**Scope for this sprint:** Use pretrained Whisper-small (`faster-whisper`) for STT and a pretrained ASVspoof checkpoint for spoof detection. **Do not train either from scratch** — this is the single highest-risk item in the whole project.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Save any fine-tuned checkpoints under `models/voice/`.

**Deliverables:** `agents/voice_agent/{predict.py, main.py}` returning contract-shaped JSON.

**Done when:** STT + spoof detection work end-to-end on a sample recording. Stop here — do not add emotion detection unless there are days to spare.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
