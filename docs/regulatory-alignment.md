# Regulatory Alignment (High-Level Overview)

NeuroForge is a **research/simulation-only framework** — it never processes real patient data, performs human trials, or deploys devices. All operations remain synthetic/hypothetical.

However, the framework is designed with awareness of real-world regulatory pathways for eventual BCI translation (e.g., Neuralink-style implantable systems).

## FDA (United States)
- **Class III high-risk implantable BCI** — typically requires **Premarket Approval (PMA)** pathway (most stringent, clinical data required).
- Early development: **Investigational Device Exemption (IDE)** for human feasibility/pivotal trials.
- Adaptive AI elements (e.g., decoding algorithms): Potential **Predetermined Change Control Plan (PCCP)** under SaMD/AI guidance (2025 draft updates emphasize lifecycle management).
- Breakthrough Devices Program or Early Feasibility Study (EFS) can accelerate access.
- Biocompatibility: Follow **ISO 10993** series (esp. Part 1 risk management, Part 6 implantation tests for local effects, chronic/chronic toxicity for long-term implants).
- Guidance: FDA 2021+ implantable BCI non-clinical testing recommendations.

## EU MDR (Medical Device Regulation)
- **Class III implantable active devices** (most BCIs) — require **conformity assessment** by Notified Body (full QMS audit + technical file review).
- **Post-Market Clinical Follow-up (PMCF)** mandatory for ongoing safety/performance data.
- Transitional provisions extended (some to 2027–2028), but full compliance expected by late 2020s for new high-risk devices.
- AI-enabled functions: Increasing scrutiny on explainability, validation, and change management.

## Key Constraints in NeuroForge
- **No real biological/trial data** — only synthetic signals and public-domain literature.
- **Mandatory HITL gates** before any "deployment simulation" or high-risk output.
- **Audit trail** anchored (file-based now, future blockchain option) for traceability.
- **Biocompatibility focus**: Agents prioritize chronic stability, immune response modeling (hypothetical only).
- Future: Export templates for IDE pre-sub, PMA modules, or EU technical documentation.

This is **not legal advice** — consult regulatory experts/FDA pre-submission or Notified Body for any real device path.

Last updated: February 2026
