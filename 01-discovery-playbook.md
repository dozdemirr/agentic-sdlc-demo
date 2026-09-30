# Phase 1 — System Discovery Playbook

> **Purpose**: Build a factual inventory of the codebase so the team has a shared,
> written understanding of what exists. This is the foundation everything else builds on.
>
> **Time**: 2–4 hours (manual) | 15–30 minutes (assisted)
>
> **Agent**: `01-discovery` | **Skill**: `system-discovery`

---

## Why This Phase Matters

Most systems older than a few years have **knowledge drift** — the people who built it
have moved on, documentation is stale or missing, and no single person understands the
full picture. This phase fixes that by creating a factual, evidence-based inventory.

Without this, every subsequent decision is based on assumptions. Assumptions are how
projects overrun.

---

## What You're Looking For

By the end of this phase, you should be able to answer:

1. What programming languages and frameworks are used?
2. What is the directory structure and what does each area contain?
3. What databases or data stores does the system connect to?
4. How does the system start up and what configuration controls it?
5. What are the largest/most complex areas of the code?
6. What external systems does it integrate with?
7. Is there any automated testing or CI/CD?
8. **What don't we know** — and how would we find out?

---

## Steps

### Step 1: Technology Identification

Open the repository root and identify:

- [ ] **Languages** — check file extensions (`.cs`, `.java`, `.py`, `.p`, `.js`, `.ts`, etc.)
- [ ] **Frameworks** — check for manifests (`package.json`, `*.csproj`, `pom.xml`, `requirements.txt`, `.pf`)
- [ ] **Databases** — check config files for connection strings, database names, ports
- [ ] **Build system** — look for `Makefile`, `Jenkinsfile`, `Dockerfile`, `.github/workflows/`, `build.*`
- [ ] **Tests** — search for directories or files containing `test`, `spec`, `Test`

```powershell
# PowerShell — file type distribution
Get-ChildItem -Recurse -File | Group-Object Extension |
    Sort-Object Count -Descending | Select-Object Count, Name -First 20
```

```bash
# Bash — file type distribution
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

### Step 2: Structure Mapping

For each top-level directory, determine:

- [ ] **Classification** — source, config, compiled output, assets, docs, tests, infrastructure?
- [ ] **File count** — how big is it?
- [ ] **Purpose** — what business function does this area serve?

```powershell
# PowerShell — directory sizes
Get-ChildItem -Directory | ForEach-Object {
    $count = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue).Count
    [PSCustomObject]@{ Name = $_.Name; Files = $count }
} | Sort-Object Files -Descending | Format-Table
```

```bash
# Bash — directory sizes
for d in */; do echo "$(find "$d" -type f | wc -l) $d"; done | sort -rn
```

### Step 3: Deep Sampling (Top 5 Modules)

For the 5 largest directories:

- [ ] Open **10 representative files** and read the first 30–50 lines
- [ ] Note: What does this file do? What's its purpose?
- [ ] Note: What database tables or APIs does it reference?
- [ ] Note: What other modules does it call, import, or include?
- [ ] Note: Any inline comments explaining business rules or history?

**Don't just count files — read them.** The purpose is to understand what each module
*does for the business*, not just what it contains.

### Step 4: Configuration Analysis

Read **every** configuration file completely:

- [ ] **Connection strings** — what databases, what hosts, what ports?
- [ ] **Environment values** — what's hardcoded vs configurable?
- [ ] **Feature flags** — what can be toggled?
- [ ] **Security** — passwords in plain text? SSL disabled? Hardcoded IPs?
- [ ] **Impact** — for each setting, what happens if you change it?

### Step 5: Entry Point Identification

How does the system start?

- [ ] **Client/UI entry** — main window, index page, app startup
- [ ] **Server/API entry** — service startup, web server config
- [ ] **Batch/scheduled** — cron jobs, queue processors, scheduled tasks
- [ ] **Integration** — webhooks, message consumers, file watchers

### Step 6: Document What You Don't Know

**This is the most important step.** Write down everything you couldn't determine:

For each unknown:
- What is unknown?
- Why does it matter? (What decisions are blocked?)
- How could you resolve it? (Who to ask, what system to inspect?)

---

## Level 2: Using the 01-Discovery Agent

Instead of doing the above manually, invoke the `01-discovery` agent:

```
@01-discovery Inventory this repository.

Identify languages, frameworks, modules, databases, entry points,
configuration, and create an unknowns register.
For each module, provide a 3–5 sentence description of its business purpose.
Flag anything inferred as [INFERRED].
```

Or use the skill directly in Copilot Chat:

```
Using the system-discovery skill, please inventory this repository.
Identify languages, frameworks, modules, databases, entry points,
configuration, and create an unknowns register.
For each module, provide a 3-5 sentence description of its business purpose.
```

### What to Review in the Output:
- Are module descriptions specific enough? ("pension calculations engine" not "pca module")
- Are database tables correctly identified with access patterns?
- Is the unknowns register honest? Did the AI flag things it couldn't determine?
- Are confidence markers present? (What's proven from the code vs guessed from names?)

### Common AI Shortcomings:
- Restating folder names as descriptions instead of explaining business purpose
- Presenting inferences as facts without flagging uncertainty
- Missing configuration parameters or not explaining their impact
- Not reading enough files (counting without sampling content)

---

## Completion Checklist

- [ ] Technology stack identified with evidence (which files prove it)
- [ ] Every major module has a **3–5 sentence** business purpose description
- [ ] Configuration files documented with parameter impact explanations
- [ ] Entry points identified and startup sequence described
- [ ] Database connections and table access patterns catalogued
- [ ] Top 5 complexity hotspots identified with file counts and rationale
- [ ] Unknowns register has **10+** items with resolution paths
- [ ] Glossary of domain-specific abbreviations compiled

## Next Phase
→ [02-documentation-playbook.md](02-documentation-playbook.md)
