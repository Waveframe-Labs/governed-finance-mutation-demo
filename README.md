# Governed Mutation Pipeline Demo (Finance Example)

**Stop AI-generated changes from approving themselves, bypassing controls, or reaching production.**

This repository demonstrates a **deterministic enforcement pipeline** that evaluates a proposed system mutation and decides:

* ✅ **Allow commit**
* ❌ **Block commit**

No ambiguity. No “we’ll catch it later.”
If the rules fail, the change never happens.

---

## Why This Exists

AI systems can propose changes faster than humans can review them.

That’s a problem.

This demo shows how to enforce **non-negotiable governance rules** — like separation of duties — *before* a change is accepted.

**Example:**
Prevent a single person (or AI acting on their behalf) from both proposing *and* approving a financial decision.

---

## What This Demo Does

This is a **fully runnable, end-to-end pipeline** that:

1. Takes a proposed system mutation
2. Binds it to a governance contract
3. Builds a structured execution run
4. Validates it through CRI-CORE
5. Produces a **deterministic commit decision**

**There is no partial success, no warning state, and no override.**
The system either allows the change — or blocks it completely.

**Output is always one of two things:**

* ✅ `COMMIT ALLOWED`
* ❌ `COMMIT BLOCKED`

---

## Scenario: Finance — Budget Reallocation

An AI system proposes reallocating budget between departments.

### Required Roles

* `proposer` → AI system
* `responsible` → Finance Manager
* `accountable` → CFO

### Rule Enforced

**Separation of duties:**

* `responsible` and `accountable` must be **different people**

---

## Demo Runs

### ❌ Blocked Case (Invalid)

Finance Manager is assigned to both roles:

* `responsible`
* `accountable`

**Result:**

```
independence: FAIL
COMMIT BLOCKED
```

**Why it fails:**
One person cannot approve their own financial decision.

---

### ✅ Allowed Case (Valid)

Roles are separated:

* `responsible` → Finance Manager
* `accountable` → CFO

**Result:**

```
independence: PASS
COMMIT ALLOWED
```

---

## How the Pipeline Works

```
Policy (finance_policy.json)
        ↓
Contract Compiler
        ↓
Compiled Contract
        ↓
Proposal Normalization
        ↓
Structured Run
        ↓
CRI-CORE Enforcement
        ↓
Commit Decision (ALLOW / BLOCK)
```

This pipeline turns a proposed change into a **governed execution that must pass validation before it can commit.**

CRI-CORE acts as a **gatekeeper** — a change cannot proceed unless all validation stages pass.

---

## Run the Demo

Install dependencies:

```
pip install -r requirements.txt
```

Run:

```
python -m runner.run_demo
```

---

## Expected Output

```
Running BLOCKED scenario...

independence: FAIL
COMMIT BLOCKED

Running ALLOWED scenario...

independence: PASS
COMMIT ALLOWED
```

---

## How This Would Be Used

**This pipeline is designed to sit directly in front of execution.**

In a real system:

1. An AI (or user) proposes a change
2. The proposal is normalized into a standard format
3. A governance contract is applied
4. CRI-CORE validates the run
5. The system:

   * allows the change
   * or blocks it before execution

This can sit in front of:

* CI/CD pipelines
* financial systems
* autonomous agents
* compliance-critical workflows

---

## What This Proves

* Unsafe changes can be **stopped before they happen**
* Governance rules can be **enforced programmatically**
* Responsibility can be **validated structurally, not assumed**
* AI systems can be **constrained without removing autonomy**

---

## Who This Is For

This demo is relevant for:

### Engineering & Platform Teams

* Enforcing constraints at the commit or deployment boundary
* Preventing invalid system changes from reaching production

### AI / ML Teams

* Controlling autonomous or semi-autonomous agent behavior
* Ensuring AI-generated actions meet governance requirements

### Compliance & Risk Teams

* Enforcing separation of duties and accountability rules
* Reducing risk in financial or regulated workflows

### Organizations Deploying AI Systems

* Adding deterministic safeguards before execution
* Moving from “monitoring” → **enforcement**

---

## Status

Early-stage demonstration of CRI-CORE enforcement capabilities.

---

<div align="center">
  <sub>© 2026 Waveframe Labs</sub>
</div>
