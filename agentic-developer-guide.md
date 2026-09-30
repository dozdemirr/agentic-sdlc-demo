# The Agentic Developer — Operating Guide

> **Purpose**: Define what it means to work as an agentic developer in an AI-augmented
> modernisation programme. This guide describes the mindset shift, the daily workflow,
> and the validation discipline required to be an effective human-in-the-loop.
>
> **Audience**: Developers at Level 2–4 on the [adoption ladder](README.md)
>
> **Prerequisite**: Read the [README](README.md) and complete the [maturity assessment](maturity-assessment.md)

---

## What Is an Agentic Developer?

An agentic developer **directs AI agents to produce work, then validates, corrects,
and approves the output**. The primary output shifts from code to decisions.

This is not "using autocomplete." It is a fundamentally different operating mode:

| Traditional Developer | Agentic Developer |
|---|---|
| Writes code from scratch | Directs agents to draft, reviews and corrects output |
| Reads the codebase manually to understand it | Invokes discovery agents, validates their findings |
| Writes tests by hand | Uses test-synthesis to generate scaffolding, then refines |
| Designs architecture alone | Reviews agent-proposed architecture, applies judgement |
| Documents after the fact | Triggers documentation agents, ensures factual accuracy |
| Owns the keyboard | **Owns the approval gate** — the PR, the go/no-go, the "is this right?" |

The developer remains accountable for quality. The AI is an acceleration layer,
not a decision authority.

---

## The Inner Loop

Every unit of agentic work follows the same cycle, regardless of task type:

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  FRAME   │────▶│  INVOKE   │────▶│  REVIEW   │────▶│  DECIDE   │
│ the task │     │ the agent │     │ the output│     │ accept /  │
│          │     │           │     │           │     │ correct / │
│          │     │           │     │           │     │ reject    │
└─────────┘     └──────────┘     └──────────┘     └─────┬─────┘
      ▲                                                  │
      └──────────────── if correcting ───────────────────┘
```

### 1. Frame — Define what you need

Before invoking any agent, be explicit about:
- **What** you want produced (document, code, tests, analysis)
- **Scope** boundaries (which module, which slice, what's excluded)
- **Inputs** the agent should reference (existing docs, code paths, constraints)
- **Quality bar** (what "good enough" looks like)

Poor framing is the most common cause of bad agent output. See the
[Prompt Guide](prompt-guide.md) for templates.

### 2. Invoke — Run the agent or skill

Use the appropriate agent for the task. Agents are numbered in the order you
should run them — this makes it clear what comes next.

| # | Task Type | Agent |
|---|---|---|
| 1 | Understand the codebase | `01-discovery` |
| 2 | Document current state | `02-documentation` |
| 3 | Identify domain boundaries | `03-domain-analysis` |
| 4 | Design target architecture | `04-modernisation` |
| 5 | Establish test safety net | `05-testing` |
| 6 | Define migration slices | `06-candidate-slices` |
| 7 | Plan the programme | `07-intelligent-migration` |
| 8 | Assess security posture | `08-security` |

> Agents 01–06 run in sequence. Agents 07–08 run when needed, not necessarily in order.

### 3. Review — Validate the output

This is where the agentic developer earns their role. Review criteria differ
by output type (see [Review Checklists](#review-checklists-by-output-type) below).

The default posture is **trust but verify**:
- At Level 2: verify everything before accepting
- At Level 3: verify structure and key claims, spot-check details
- At Level 4: review flagged items and exceptions only

### 4. Decide — Accept, correct, or reject

| Decision | When | Action |
|---|---|---|
| **Accept** | Output meets quality bar, evidence checks out | Commit / approve the PR |
| **Correct** | Output is structurally right but has specific errors | Fix the errors, re-run validation, then accept |
| **Reject and re-invoke** | Output missed the point or used wrong inputs | Reframe the prompt with better context, re-invoke |
| **Reject and do manually** | Agent is consistently wrong on this task | Do the work yourself — some tasks don't suit agents yet |

---

## Review Checklists by Output Type

### Reviewing Agent-Generated Documentation

- [ ] **File references are real** — click/search every cited file path
- [ ] **Descriptions are specific** — "calculates premium based on risk factors" not "handles pricing"
- [ ] **Confidence is marked** — does it distinguish proven facts from inferences?
- [ ] **Unknowns are honest** — did it flag things it couldn't determine?
- [ ] **Diagrams match reality** — do component relationships reflect actual code dependencies?
- [ ] **No future-state language** — does it describe what *is*, not what *should be*?

### Reviewing Agent-Generated Tests

- [ ] **Tests actually test something** — not just asserting `true == true`
- [ ] **Assertions are meaningful** — checking business outcomes, not implementation details
- [ ] **Edge cases covered** — nulls, empty collections, boundary values
- [ ] **Deterministic** — no time-dependent or order-dependent tests
- [ ] **Naming** — test names describe the behaviour being verified
- [ ] **No test pollution** — tests clean up after themselves

### Reviewing Agent-Generated Architecture/Design

- [ ] **Traceable to code** — proposed boundaries align with actual code structure
- [ ] **Feasible with current team** — does the team have the skills for this?
- [ ] **Incremental** — can it be delivered slice by slice, not big-bang?
- [ ] **Risk-aware** — are shared-write tables, auth changes, and schema migrations called out?

### Reviewing Agent-Generated Candidate Slices

- [ ] **Every slice maps to a target architecture component** — no orphan slices
- [ ] **First slice is genuinely lowest risk** — not just the most interesting one
- [ ] **Scope is explicit** — both "in" and "out" are stated, not implied
- [ ] **No slice spans multiple bounded contexts** — if it does, it needs splitting
- [ ] **Rollback approach is realistic** — not just "revert the PR"
- [ ] **Dependencies are consistent** — no circular refs, ordering makes sense
- [ ] **Complexity estimates are honest** — agent tends to underestimate shared-write risks
- [ ] **Rollback considered** — every step has a back-out plan

---

## When to Stop Trusting the Agent

Escalate to manual work when:

| Signal | What It Means | Action |
|---|---|---|
| Agent cites files that don't exist | It's hallucinating context | Do the discovery manually |
| Same error after 2 correction cycles | The task doesn't suit agents | Write it yourself |
| Output contradicts existing documentation | Agent didn't read inputs properly | Re-invoke with explicit input references, or do manually |
| Security-sensitive code generated | Agent may miss edge cases | Write security code yourself, use agent for tests only |
| Agent proposes scope beyond the slice | It's over-reaching | Reject, reframe with strict scope |
| Confidence is low and you can't verify | You don't know enough to validate | Learn the area first (Level 1), then return to Level 2 |

---

## Agentic Developer by Adoption Level

### Level 2 — Assisted

**Your day**: Invoke one agent at a time. Review every output in full. Accept, correct,
or reject. Move to the next step manually.

- You choose when to invoke an agent
- You choose which agent/skill to use
- You review 100% of output
- You decide when to proceed to the next phase

**Time split**: ~40% framing and invoking, ~50% reviewing, ~10% correcting

### Level 3 — Guided

**Your day**: The pipeline runs through stages, pausing at each checkpoint for your approval.
You review structure and key claims, spot-check details.

- Agents suggest the next step
- You approve or redirect at each gate
- You review structure and key claims (~70% of output)
- You spot-check details on high-risk areas

**Time split**: ~20% framing, ~50% reviewing, ~20% correcting, ~10% steering

### Level 4 — Supervised

**Your day**: The pipeline runs. You get alerts on flagged decisions, uncertainty,
or quality gate failures. You intervene when needed.

- Agents run through stages autonomously
- You review flagged items and exceptions only
- You validate at phase gates (go/no-go decisions)
- You handle escalations

**Time split**: ~10% framing, ~30% reviewing flagged items, ~10% correcting, ~50% other work

---

## Skills to Develop

| Skill | Why It Matters | How to Build It |
|---|---|---|
| **Prompt precision** | Vague prompts produce vague output | Use the [Prompt Guide](prompt-guide.md); iterate on what works |
| **Output validation** | You're the quality gate | Practice reviewing agent output against the codebase; compare to manual results |
| **Knowing when to stop** | Some tasks don't suit agents | Track correction cycles; if you're correcting more than creating, do it manually |
| **Scope discipline** | Agents will over-produce if you let them | Always define what's in and what's out before invoking |
| **Pattern recognition** | Recognise when agent output "looks right but isn't" | Compare early outputs to manually-produced equivalents; build intuition |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|---|---|---|
| **Rubber-stamping** — accepting output without review | Bugs, hallucinations, and drift compound silently | Review against the checklist for the output type |
| **Over-prompting** — giving 500-word instructions for a simple task | Agent gets confused, ignores half the constraints | Keep prompts focused; one task per invocation |
| **Under-prompting** — "write me some tests" | Agent guesses scope, produces irrelevant output | Specify scope, inputs, and quality bar |
| **Agent shopping** — trying every agent until one gives the right answer | Wastes time, indicates you don't understand the task yet | Read the playbook first, choose the right agent/skill |
| **Skipping manual understanding** — using agents before you understand the system | You can't validate what you don't understand | Do Phase 1 manually at least once |

---

## Summary

Being an agentic developer means:

1. **You direct** — agents execute
2. **You validate** — agents draft
3. **You decide** — agents suggest
4. **You're accountable** — agents are tools

The agent produces the first draft. You produce the final product.
