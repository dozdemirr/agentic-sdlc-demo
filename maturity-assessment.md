# Maturity Self-Assessment Worksheet

> **Purpose**: Determine your team's current readiness level and build a concrete
> plan to progress. Be honest — overestimating sets adoption back further than
> starting lower.

---

## Part 1: Score Your Team

**0** = Not at all | **1** = Partially | **2** = Fully

### A. AI Familiarity
| # | Statement | Score |
|---|---|---|
| A1 | Team members use AI code assistants (Copilot, Cursor, etc.) regularly | /2 |
| A2 | Someone on the team has used AI chat to ask questions about code | /2 |
| A3 | Team understands that AI output needs validation, not blind trust | /2 |
| A4 | Team has corrected an AI-generated output at least once | /2 |
| A5 | Management supports experimentation with AI tooling | /2 |
| | **Subtotal A** | /10 |

### B. Codebase Understanding
| # | Statement | Score |
|---|---|---|
| B1 | The team can name all major components of the system | /2 |
| B2 | The team knows which databases the system connects to | /2 |
| B3 | Someone can trace a user action end-to-end through the code | /2 |
| B4 | The team knows where configuration is stored and what it controls | /2 |
| B5 | The team knows the deployment process (even if manual) | /2 |
| | **Subtotal B** | /10 |

### C. Process Maturity
| # | Statement | Score |
|---|---|---|
| C1 | The team uses version control effectively (branches, PRs, reviews) | /2 |
| C2 | There is some form of automated testing (even minimal) | /2 |
| C3 | There is a defined release/deployment process | /2 |
| C4 | Technical decisions are documented somewhere | /2 |
| C5 | There is dedicated time for modernisation / tech debt | /2 |
| | **Subtotal C** | /10 |

### D. Trust in Automation
| # | Statement | Score |
|---|---|---|
| D1 | Team is willing to try AI-generated documentation | /2 |
| D2 | Team would trust an AI-identified risk list (after review) | /2 |
| D3 | Team would let AI produce a first draft of an architecture document | /2 |
| D4 | Team would let AI suggest code changes (with human review) | /2 |
| D5 | Budget/time is allocated for tooling adoption | /2 |
| | **Subtotal D** | /10 |

---

## Part 2: Your Level

| Total Score | Starting Level |
|---|---|
| 0–10 | **Level 1 — Manual**: Follow the playbooks by hand |
| 11–20 | **Level 2 — Assisted**: Run agents one at a time, review closely |
| 21–30 | **Level 3 — Guided**: Let agents run, review at each checkpoint |
| 31–35 | **Level 4 — Supervised**: Monitor, intervene on flagged items only |
| 36–40 | **Level 5 — Autonomous**: Periodic review of outputs |

**Your score**: _____ / 40 → **Level**: _____

---

## Part 3: Address Your Weakest Area

| Weakest Area | Recommended Action |
|---|---|
| **A (AI Familiarity)** | Spend 1 hour per week using AI chat on your codebase. Ask questions. Correct mistakes. |
| **B (Codebase Understanding)** | This is exactly what Phase 1 (Discovery) solves. Run it manually first. |
| **C (Process Maturity)** | Foundational — focus on version control and deployment before AI adoption. |
| **D (Trust in Automation)** | Start with read-only operations (discovery, documentation). Nothing changes code. |

---

## Part 4: Progression Timeline

| Week | Activity | Target |
|---|---|---|
| 1 | Run Phase 1 (Discovery) manually using playbook | Level 1 |
| 2 | Review output as team. Run Phase 1 with AI. Compare results. | 1 → 2 |
| 3 | Run Phase 2 (Documentation) with AI. Review output. | Level 2 |
| 4 | Run Phase 3 (Domain Analysis) with AI. Review output. | Level 2 |
| 5–6 | Repeat Phases 1–3 on a second system/module. Build pattern recognition. | 2 → 3 |
| 7–8 | Let the AI suggest next steps at each checkpoint. Review and approve. | Level 3 |
| 9–12 | Full pipeline under guided mode. Review at each gate. | 3 → 4 |

> Don't skip levels. Each one builds the trust needed for the next.

---

## Part 5: Success Metrics

| Transition | You're Ready When |
|---|---|
| 1 → 2 | Team can explain what a system inventory is and why it matters |
| 2 → 3 | Team has corrected 3+ AI outputs (proving they can validate) |
| 3 → 4 | Full pipeline completed once with zero undetected critical errors |
| 4 → 5 | Three runs with no overrides needed |

---

> The goal is not Level 5. The goal is the level where your team is
> productive and confident. Level 3 is a perfectly valid steady state.
